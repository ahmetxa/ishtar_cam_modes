#!/usr/bin/env python
"""Deterministic release builder for the ishtar_cam_modes KernelSU/Magisk module.

Faz 9.1. Produces the release archive from the tree, enforces the Faz 1.2
packaging assertions as a hard gate, and emits a manifest binding the release
to the checksums it expects.

Usage
    python scripts/build-release.py                  build into dist/
    python scripts/build-release.py --self-test      determinism + assertion tests
    python scripts/build-release.py --list           print the contents specification
    python scripts/build-release.py --source DIR --out FILE --manifest FILE

Why Python and not shell (F9.1-04 deviation, recorded as FIND-9.1-01):
    The determinism standard below requires control over every ZIP header
    field. There is no `zip` binary on the maintainer's host, and the CLI
    cannot fix entry timestamps anyway. Python's zipfile can, and Python is
    already this project's tool language (ishtar-cam-modes/tools/*.py).

Determinism standard (F9.1-03)
    BYTE-IDENTICAL across repeated builds from an unchanged source tree, on a
    given host. Achieved by fixing every field that would otherwise vary:
      - entry order: sorted by archive path, always;
      - entry timestamp: the ZIP epoch 1980-01-01 00:00:00, never the file's;
      - permissions: 0644 for every entry (customize.sh re-applies the real
        modes at install time with set_perm_recursive / set_perm);
      - create_system 0, create/extract version 20, no extra fields,
        no directory entries, no archive comment;
      - compression: deflate at a fixed level.
    The one field outside this script's control is the deflate stream itself,
    which is produced by the host zlib. Two builds on one host are
    byte-identical; two builds on hosts with different zlib builds may differ
    in compressed bytes while remaining content-identical. Compare with
    --self-test on one host; compare entry checksums across hosts.

    This standard is about self-reproducibility. It is NOT a claim of byte
    identity with any previously shipped archive: ishtar-cam-modes-v2.1.zip
    predates changes now in the tree.
"""

import argparse
import fnmatch
import hashlib
import os
import shutil
import sys
import tempfile
import zipfile

MODULE_DIR = "ishtar-cam-modes"

# The HAL binary halpatch.sh deliberately does not ship (halpatch.sh:34).
HAL_SIZE = 27268688
# Between the largest legitimate entry (a 1,062,250-byte sensor blob) and the
# HAL binary. Any entry at or above this is the size class Faz 1.2 forbids.
MAX_ENTRY_SIZE = 8 * 1024 * 1024

ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)
ENTRY_MODE = 0o100644
COMPRESS_LEVEL = 9

# --- Contents specification (F9.1-01) --------------------------------------
# Every file under MODULE_DIR must match exactly one rule below. A file that
# matches neither is UNCLASSIFIED and fails the build (assertion A3): a new
# file in the module directory is a release decision, not a silent inclusion.

INCLUDE = [
    # Module surface KernelSU/Magisk reads at install and at boot.
    ("Kullanim.txt", "user documentation shipped with the module"),
    ("action.sh", "KernelSU action button entry point"),
    ("customize.sh", "installer: device gate, blob/HAL md5 gate, permissions"),
    ("halpatch.sh", "50MP HAL patch layer, sourced by post-fs-data.sh"),
    ("module.prop", "module identity and version"),
    ("post-fs-data.sh", "boot-time bind mount of the sensor blob and HAL"),
    ("service.sh", "late_start service hook"),
    ("setmode.sh", "mode dispatch"),
    ("tile-app.apk", "prebuilt QuickSettings tile app (F9.1-02: prebuilt)"),
    ("blobs/*.bin", "the nine dispatchable sensor blobs"),
    ("blobs/hal-fullres.patch", "the 16-point HAL patch table"),
    ("webroot/*", "KernelSU WebUI"),
    # Tile app sources ship for build transparency, as in v1.0..v2.1.
    ("tile-app/*", "tile app manifest and build script (direct children only)"),
    ("tile-app/java/**/*.java", "tile app java sources"),
    ("tile-app/res/**/*.xml", "tile app resources"),
    ("tools/*.py", "host tools that regenerate the sensor blobs"),
]

EXCLUDE = [
    ("mode", "live working state; absent, post-fs-data.sh:14-26 defaults to "
             "stock. Omission IS the F9.1-04 normalization (AUTOPSY-P3-03)"),
    ("lang", "live working state; absent, action.sh:185 defaults to en"),
    ("active/**", "runtime working copy of the sensor blob; duplicates blobs/ "
                  "and is seeded on device"),
    ("candidates/**", "unproven experimental blobs; no setmode.sh mode "
                      "dispatches them"),
    ("tile-app/debug.keystore", "SIGNING CREDENTIAL. Faz 1.2. Assertion A1 is "
                                "the enforcement; this rule is the belt"),
    ("tile-app/out/**", "build output; the signed apk is copied to "
                        "tile-app.apk one level up"),
    ("tools/__pycache__/**", "python bytecode cache"),
]


def _match(rel, pattern):
    """Glob match where '*' does not cross '/' but '**' does."""
    if "**" in pattern:
        return fnmatch.fnmatchcase(rel, pattern.replace("**", "*"))
    if pattern.count("/") != rel.count("/"):
        return False
    return fnmatch.fnmatchcase(rel, pattern)


def classify(rel):
    """Return ('include'|'exclude', reason) or (None, None) if unclassified."""
    for pattern, reason in EXCLUDE:
        if _match(rel, pattern):
            return "exclude", reason
    for pattern, reason in INCLUDE:
        if _match(rel, pattern):
            return "include", reason
    return None, None


def survey(source):
    """Walk the module directory and adjudicate every file."""
    root = os.path.join(source, MODULE_DIR)
    if not os.path.isdir(root):
        raise SystemExit("missing module directory: %s" % root)
    included, excluded, unclassified = [], [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            kind, reason = classify(rel)
            if kind == "include":
                included.append((rel, full, reason))
            elif kind == "exclude":
                excluded.append((rel, reason))
            else:
                unclassified.append(rel)
    included.sort(key=lambda e: e[0])
    return included, excluded, unclassified


# --- Packaging assertions (F9.1-05) ----------------------------------------
# Each raises AssertionFailure, which aborts the build. None of them warn.

class AssertionFailure(Exception):
    pass


def assert_no_credential(entries):
    """A1: no credential may enter the archive."""
    bad = [rel for rel, _full, _r in entries
           if rel.lower().endswith((".keystore", ".jks", ".p12", ".pem", ".pk8"))
           or os.path.basename(rel).lower() in ("debug.keystore", "release.keystore")]
    if bad:
        raise AssertionFailure(
            "A1 credential entry in archive: %s" % ", ".join(bad))


def assert_no_hal_size_class(entries):
    """A2: the 27 MB HAL binary must never be shipped."""
    bad = ["%s (%d bytes)" % (rel, os.path.getsize(full))
           for rel, full, _r in entries
           if os.path.getsize(full) >= MAX_ENTRY_SIZE]
    if bad:
        raise AssertionFailure(
            "A2 entry at or above the forbidden size class "
            "(limit %d, HAL binary is %d): %s"
            % (MAX_ENTRY_SIZE, HAL_SIZE, ", ".join(bad)))


def assert_no_unclassified(unclassified):
    """A3: no archive entry outside the contents specification."""
    if unclassified:
        raise AssertionFailure(
            "A3 file(s) under %s match no include or exclude rule: %s\n"
            "    Add the path to INCLUDE or EXCLUDE in this script. A new file "
            "in the module directory is a release decision."
            % (MODULE_DIR, ", ".join(unclassified)))


# --- Archive assembly ------------------------------------------------------

def module_version(source):
    prop = os.path.join(source, MODULE_DIR, "module.prop")
    with open(prop, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("version="):
                return line.split("=", 1)[1].strip()
    raise SystemExit("no version= in module.prop")


def build(source, out_path):
    included, excluded, unclassified = survey(source)

    assert_no_unclassified(unclassified)
    assert_no_credential(included)
    assert_no_hal_size_class(included)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    tmp = out_path + ".partial"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED,
                         compresslevel=COMPRESS_LEVEL) as zf:
        for rel, full, _reason in included:
            info = zipfile.ZipInfo(rel, date_time=ZIP_EPOCH)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.create_version = 20
            info.extract_version = 20
            info.external_attr = ENTRY_MODE << 16
            info.internal_attr = 0
            with open(full, "rb") as fh:
                zf.writestr(info, fh.read())
    os.replace(tmp, out_path)
    return included, excluded


def digests(path):
    md5, sha = hashlib.md5(), hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            md5.update(chunk)
            sha.update(chunk)
    return md5.hexdigest(), sha.hexdigest()


# --- Manifest (F9.1-06) ----------------------------------------------------

def write_manifest(path, archive, version, included, excluded):
    a_md5, a_sha = digests(archive)
    rows = []
    for rel, full, _reason in included:
        m, s = digests(full)
        rows.append((rel, os.path.getsize(full), m, s))

    lines = []
    lines.append("# ishtar_cam_modes Release Manifest")
    lines.append("")
    lines.append("Generated by `scripts/build-release.py`. Do not hand-edit: "
                 "regenerate it, so the checksums always describe the archive "
                 "that was actually produced (Faz 9.1 VAL-MANIFEST).")
    lines.append("")
    lines.append("## 1. Archive")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append("| File | `%s` |" % os.path.basename(archive))
    lines.append("| Module version | `%s` |" % version)
    lines.append("| Size | %d bytes |" % os.path.getsize(archive))
    lines.append("| Entries | %d |" % len(rows))
    lines.append("| md5 | `%s` |" % a_md5)
    lines.append("| sha256 | `%s` |" % a_sha)
    lines.append("")
    lines.append("The archive digest is reproducible only against a build from "
                 "the same source tree on a host with the same zlib; see the "
                 "determinism standard in `scripts/build-release.py`. The "
                 "per-entry digests below are host-independent and are the "
                 "durable binding.")
    lines.append("")
    lines.append("## 2. Entries")
    lines.append("")
    lines.append("| Path | Size | md5 | sha256 |")
    lines.append("|---|---|---|---|")
    for rel, size, m, s in rows:
        lines.append("| `%s` | %d | `%s` | `%s` |" % (rel, size, m, s))
    lines.append("")
    lines.append("## 3. Deliberate exclusions")
    lines.append("")
    lines.append("Every file under `%s/` that is not an entry above is "
                 "excluded by an explicit rule with a reason. A file matching "
                 "no rule fails the build (assertion A3)." % MODULE_DIR)
    lines.append("")
    lines.append("| Path | Reason |")
    lines.append("|---|---|")
    for rel, reason in excluded:
        lines.append("| `%s` | %s |" % (rel, reason.replace("|", "\\|")))
    lines.append("")
    lines.append("## 4. Enforced packaging assertions")
    lines.append("")
    lines.append("| ID | Assertion | Enforcement |")
    lines.append("|---|---|---|")
    lines.append("| A1 | No credential entry (`.keystore`, `.jks`, `.p12`, "
                 "`.pem`, `.pk8`). | Build aborts. |")
    lines.append("| A2 | No entry at or above %d bytes; the HAL binary is %d "
                 "and is never shipped. | Build aborts. |"
                 % (MAX_ENTRY_SIZE, HAL_SIZE))
    lines.append("| A3 | No file outside the contents specification. | "
                 "Build aborts. |")
    lines.append("")
    lines.append("Each assertion is proven to fire by "
                 "`python scripts/build-release.py --self-test`.")
    lines.append("")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    return a_md5, a_sha


# --- Self-test (F9.1-07, F9.1-08) ------------------------------------------

def _expect_failure(source, label, marker):
    out = os.path.join(tempfile.mkdtemp(), "x.zip")
    try:
        build(source, out)
    except AssertionFailure as exc:
        ok = marker in str(exc)
        print("  %-32s %s  %s" % (label, "PASS" if ok else "WRONG-ASSERTION",
                                  str(exc).splitlines()[0]))
        return ok
    print("  %-32s FAIL  build succeeded; the assertion did not fire" % label)
    return False


def self_test(source):
    print("VAL-BUILD2 - two builds from an unchanged tree")
    tmp = tempfile.mkdtemp(prefix="ishtar-rel-")
    a, b = os.path.join(tmp, "a.zip"), os.path.join(tmp, "b.zip")
    build(source, a)
    build(source, b)
    da, db = digests(a)[1], digests(b)[1]
    same = da == db
    print("  build 1 sha256 %s" % da)
    print("  build 2 sha256 %s" % db)
    print("  byte-identical: %s" % ("PASS" if same else "FAIL"))

    print("VAL-ASSERT - each assertion must fail the build")
    work = os.path.join(tmp, "tree")
    os.makedirs(work)
    shutil.copytree(os.path.join(source, MODULE_DIR),
                    os.path.join(work, MODULE_DIR))
    mod = os.path.join(work, MODULE_DIR)

    # N1: a credential at a path an include rule accepts (tile-app/*).
    n1_path = os.path.join(mod, "tile-app", "release.keystore")
    with open(n1_path, "wb") as fh:
        fh.write(b"not a real key")
    r1 = _expect_failure(work, "A1 credential entry", "A1 credential")
    os.remove(n1_path)

    # N2: an entry in the forbidden size class at a path blobs/*.bin accepts.
    n2_path = os.path.join(mod, "blobs", "zz-oversize.bin")
    with open(n2_path, "wb") as fh:
        fh.truncate(HAL_SIZE)
    r2 = _expect_failure(work, "A2 HAL size class", "A2 entry at or above")
    os.remove(n2_path)

    # N3: a file matching no include and no exclude rule.
    n3_path = os.path.join(mod, "scratch-notes.txt")
    with open(n3_path, "w") as fh:
        fh.write("stray working file\n")
    r3 = _expect_failure(work, "A3 unclassified file", "A3 file(s) under")
    os.remove(n3_path)

    # The repaired tree must build again, so the tests prove the assertions
    # and not a permanently broken copy.
    build(work, os.path.join(tmp, "c.zip"))
    print("  repaired tree builds again        PASS")

    shutil.rmtree(tmp, ignore_errors=True)
    ok = same and r1 and r2 and r3
    print("SELF-TEST: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


# --- Entry point -----------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source", default=".", help="repository root")
    ap.add_argument("--out", help="archive path (default dist/<name>-<ver>.zip)")
    ap.add_argument("--manifest", default=os.path.join("docs",
                    "release-manifest.md"), help="manifest path")
    ap.add_argument("--self-test", action="store_true",
                    help="run VAL-BUILD2 and VAL-ASSERT, build nothing")
    ap.add_argument("--list", action="store_true",
                    help="print the contents specification and exit")
    args = ap.parse_args(argv)

    source = os.path.abspath(args.source)

    if args.list:
        included, excluded, unclassified = survey(source)
        print("INCLUDED (%d)" % len(included))
        for rel, full, reason in included:
            print("  %-52s %9d  %s" % (rel, os.path.getsize(full), reason))
        print("EXCLUDED (%d)" % len(excluded))
        for rel, reason in excluded:
            print("  %-52s %s" % (rel, reason))
        if unclassified:
            print("UNCLASSIFIED (%d) - these would fail the build"
                  % len(unclassified))
            for rel in unclassified:
                print("  %s" % rel)
        return 1 if unclassified else 0

    if args.self_test:
        return self_test(source)

    version = module_version(source)
    out = args.out or os.path.join(source, "dist",
                                   "ishtar-cam-modes-%s.zip" % version)
    if os.path.abspath(os.path.dirname(out)) == source:
        raise SystemExit(
            "refusing to write into the repository root, where the shipped "
            "archives live: %s" % out)

    try:
        included, excluded = build(source, out)
    except AssertionFailure as exc:
        print("PACKAGING ASSERTION FAILED\n  %s" % exc, file=sys.stderr)
        return 2

    manifest = args.manifest
    if not os.path.isabs(manifest):
        manifest = os.path.join(source, manifest)
    a_md5, a_sha = write_manifest(manifest, out, version, included, excluded)

    print("archive  : %s" % out)
    print("version  : %s" % version)
    print("entries  : %d included, %d excluded by rule"
          % (len(included), len(excluded)))
    print("size     : %d bytes" % os.path.getsize(out))
    print("md5      : %s" % a_md5)
    print("sha256   : %s" % a_sha)
    print("manifest : %s" % manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
