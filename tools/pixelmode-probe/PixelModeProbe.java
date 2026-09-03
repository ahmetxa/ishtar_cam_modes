/*
 * PixelModeProbe -- minimal Camera2 client that requests
 * SENSOR_PIXEL_MODE = MAXIMUM_RESOLUTION on the IMX989 main sensor.
 *
 * Built for the ishtar (Xiaomi 13 Ultra) RAW payload geometry diagnosis.
 * See docs/raw-geometry-diagnosis.md sections 18-22.
 *
 * This is NOT an APK. It is a bare classes.dex run through app_process, which
 * is the standard Android shell-tool mechanism. It runs as the shell user,
 * which holds android.permission.CAMERA (granted=true, SYSTEM_FIXED).
 *
 * Purpose: IMPL-44 published ULTRA_HIGH_RESOLUTION_SENSOR and made
 * sensor.pixelMode a legal request key. Nothing had yet REQUESTED the mode.
 * This client requests it and measures what comes back.
 *
 * A null result -- pixelMode accepted but the payload still folded into one
 * quadrant -- is a real and informative outcome, not a failure of this client.
 */

import android.content.Context;
import android.graphics.ImageFormat;
import android.graphics.Rect;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.CameraMetadata;
import android.hardware.camera2.CaptureRequest;
import android.hardware.camera2.CaptureResult;
import android.hardware.camera2.TotalCaptureResult;
import android.hardware.camera2.params.OutputConfiguration;
import android.hardware.camera2.params.SessionConfiguration;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.media.Image;
import android.media.ImageReader;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.Looper;
import android.util.Size;
import android.view.Surface;

import java.io.FileOutputStream;
import java.lang.reflect.Method;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executor;
import java.util.concurrent.TimeUnit;

public class PixelModeProbe {

    private static final String CAMERA_ID = "2";      // IMX989 main sensor; AGC uses this id

    // Settable from argv so the same instrument can probe a geometry the
    // max-res stream table actually permits. Defaults to the unbinned geometry.
    //   usage: PixelModeProbe [width] [height] [max|default|both]
    private static int WIDTH = 8192;
    private static int HEIGHT = 6144;
    private static String MODES = "both";
    private static int FORCE_FORMAT = -1;

    private static final long TIMEOUT_SEC = 20;
    private static final String OUT_DIR = "/data/local/tmp/";

    private static Handler handler;
    private static CameraManager cameraManager;

    private static void log(String s) {
        System.out.println(s);
        System.out.flush();
    }

    private static void section(String s) {
        log("");
        log("=== " + s + " ===");
    }

    public static void main(String[] args) {
        int exit = 0;
        try {
            realMain(args);
        } catch (Throwable t) {
            log("FATAL: " + t);
            t.printStackTrace(System.out);
            exit = 1;
        }
        System.out.flush();
        // app_process will not exit on its own while the HandlerThread lives.
        System.exit(exit);
    }

    private static void realMain(String[] args) throws Exception {
        if (args.length >= 2) {
            WIDTH = Integer.parseInt(args[0]);
            HEIGHT = Integer.parseInt(args[1]);
        }
        if (args.length >= 3) {
            MODES = args[2];
        }
        if (args.length >= 4) {
            FORCE_FORMAT = Integer.parseInt(args[3]);
        }
        log("probe geometry: " + WIDTH + "x" + HEIGHT + "  modes=" + MODES);

        section("CONTEXT");
        Context ctx = acquireContext();
        log("context: " + ctx);

        HandlerThread ht = new HandlerThread("probe");
        ht.start();
        handler = new Handler(ht.getLooper());

        cameraManager = (CameraManager) ctx.getSystemService(Context.CAMERA_SERVICE);
        log("cameraManager: " + cameraManager);
        log("cameraIdList: " + Arrays.toString(cameraManager.getCameraIdList()));

        section("CHARACTERISTICS (camera " + CAMERA_ID + ")");
        CameraCharacteristics cc = cameraManager.getCameraCharacteristics(CAMERA_ID);

        // -- capability gate: abort loudly if UHR is not published --------------
        int[] caps = cc.get(CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES);
        log("availableCapabilities: " + Arrays.toString(caps));
        boolean uhr = false;
        if (caps != null) {
            for (int c : caps) {
                if (c == CameraMetadata.REQUEST_AVAILABLE_CAPABILITIES_ULTRA_HIGH_RESOLUTION_SENSOR) {
                    uhr = true;
                }
            }
        }
        log("ULTRA_HIGH_RESOLUTION_SENSOR present: " + uhr);
        if (!uhr) {
            throw new IllegalStateException(
                "ABORT: camera " + CAMERA_ID + " does not advertise "
                + "ULTRA_HIGH_RESOLUTION_SENSOR. The IMPL-44 patch is not live. "
                + "Verify the HAL md5 before continuing.");
        }

        log("SENSOR_INFO_ACTIVE_ARRAY_SIZE            : "
            + cc.get(CameraCharacteristics.SENSOR_INFO_ACTIVE_ARRAY_SIZE));
        log("SENSOR_INFO_PIXEL_ARRAY_SIZE             : "
            + cc.get(CameraCharacteristics.SENSOR_INFO_PIXEL_ARRAY_SIZE));
        log("..ACTIVE_ARRAY_SIZE_MAXIMUM_RESOLUTION   : "
            + safeGet(cc, CameraCharacteristics.SENSOR_INFO_ACTIVE_ARRAY_SIZE_MAXIMUM_RESOLUTION));
        log("..PIXEL_ARRAY_SIZE_MAXIMUM_RESOLUTION    : "
            + safeGet(cc, CameraCharacteristics.SENSOR_INFO_PIXEL_ARRAY_SIZE_MAXIMUM_RESOLUTION));
        log("SENSOR_INFO_BINNING_FACTOR               : "
            + safeGet(cc, CameraCharacteristics.SENSOR_INFO_BINNING_FACTOR));

        // -- the two stream maps ------------------------------------------------
        section("DEFAULT STREAM MAP");
        StreamConfigurationMap def = null;
        try {
            def = cc.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);
            dumpRawSizes(def, "default");
        } catch (Throwable t) {
            log("default stream map threw: " + t);
        }

        section("MAXIMUM_RESOLUTION STREAM MAP");
        log("NOTE: d0015/d0016 (min frame durations / stall durations "
            + "MaximumResolution) are known ABSENT on this build -- their source "
            + "arrays are empty. The key list advertises 851989/851990 while "
            + "get() may return null. A throw HERE is that known gap, not a bug "
            + "in this client.");
        StreamConfigurationMap max = null;
        try {
            max = cc.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP_MAXIMUM_RESOLUTION);
            if (max == null) {
                log("RESULT: max-res stream map is NULL (no throw). "
                    + "This is the d0015/d0016 gap.");
            } else {
                dumpRawSizes(max, "max-res");
            }
        } catch (Throwable t) {
            log("RESULT: max-res stream map THREW -- this is the known "
                + "d0015/d0016 gap (Faz4.2 duration-row work), not a client bug:");
            log("  " + t);
        }

        // -- choose a format ----------------------------------------------------
        int format = (FORCE_FORMAT > 0) ? FORCE_FORMAT : chooseFormat(max, def);
        if (FORCE_FORMAT > 0) log("format FORCED by argv: " + fmtName(format));
        log("");
        log("chosen format: " + fmtName(format) + " (0x"
            + Integer.toHexString(format) + ") at " + WIDTH + "x" + HEIGHT);

        // -- the two captures ---------------------------------------------------
        String tag = "_" + WIDTH + "x" + HEIGHT;
        if (!"default".equals(MODES)) {
            section("CAPTURE -- pixelMode = MAXIMUM_RESOLUTION");
            runCapture(format, true, OUT_DIR + "probe_max" + tag);
        }
        if (!"max".equals(MODES)) {
            section("CAPTURE -- CONTROL, pixelMode = DEFAULT");
            runCapture(format, false, OUT_DIR + "probe_default" + tag);
        }

        section("DONE");
    }

    /**
     * app_process has no Application. This is the standard shell-tool route to a
     * Context: ActivityThread.systemMain() then getSystemContext(). Both are
     * hidden API, so they are reached by reflection.
     */
    private static Context acquireContext() throws Exception {
        try {
            Looper.prepareMainLooper();
        } catch (IllegalStateException e) {
            // already prepared by systemMain in some builds -- fine
        }
        Class<?> at = Class.forName("android.app.ActivityThread");
        Method systemMain = at.getMethod("systemMain");
        Object thread = systemMain.invoke(null);
        Method getSystemContext = at.getMethod("getSystemContext");
        return (Context) getSystemContext.invoke(thread);
    }

    private static Object safeGet(CameraCharacteristics cc, CameraCharacteristics.Key<?> k) {
        try {
            Object v = cc.get(k);
            if (v instanceof int[]) return Arrays.toString((int[]) v);
            return String.valueOf(v);
        } catch (Throwable t) {
            return "<threw " + t.getClass().getSimpleName() + ": " + t.getMessage() + ">";
        }
    }

    private static void dumpRawSizes(StreamConfigurationMap m, String label) {
        if (m == null) {
            log(label + ": null");
            return;
        }
        int[] formats = m.getOutputFormats();
        log(label + " output formats: " + Arrays.toString(formats));
        for (int f : formats) {
            if (f == ImageFormat.RAW_SENSOR || f == ImageFormat.RAW10
                || f == ImageFormat.RAW12 || f == ImageFormat.RAW_PRIVATE) {
                Size[] sizes = m.getOutputSizes(f);
                log("  " + fmtName(f) + " (0x" + Integer.toHexString(f) + "): "
                    + (sizes == null ? "null" : Arrays.toString(sizes)));
            }
        }
    }

    private static boolean mapHas(StreamConfigurationMap m, int format) {
        if (m == null) return false;
        try {
            Size[] sizes = m.getOutputSizes(format);
            if (sizes == null) return false;
            for (Size s : sizes) {
                if (s.getWidth() == WIDTH && s.getHeight() == HEIGHT) return true;
            }
        } catch (Throwable ignored) {
        }
        return false;
    }

    /** Prefer RAW_SENSOR (16-bit, unambiguous to measure) over packed RAW10. */
    private static int chooseFormat(StreamConfigurationMap max, StreamConfigurationMap def) {
        int[] prefer = { ImageFormat.RAW_SENSOR, ImageFormat.RAW10, ImageFormat.RAW12 };
        for (int f : prefer) {
            if (mapHas(max, f)) {
                log("format " + fmtName(f) + " found at " + WIDTH + "x" + HEIGHT
                    + " in the MAX-RES map");
                return f;
            }
        }
        for (int f : prefer) {
            if (mapHas(def, f)) {
                log("format " + fmtName(f) + " found at " + WIDTH + "x" + HEIGHT
                    + " in the DEFAULT map");
                return f;
            }
        }
        log("WARNING: " + WIDTH + "x" + HEIGHT + " not listed in either map; "
            + "falling back to RAW_SENSOR and letting the framework rule on it. "
            + "A configuration failure here is itself informative.");
        return ImageFormat.RAW_SENSOR;
    }

    private static String fmtName(int f) {
        if (f == ImageFormat.RAW_SENSOR) return "RAW_SENSOR";
        if (f == ImageFormat.RAW10) return "RAW10";
        if (f == ImageFormat.RAW12) return "RAW12";
        if (f == ImageFormat.RAW_PRIVATE) return "RAW_PRIVATE";
        if (f == ImageFormat.JPEG) return "JPEG";
        return "fmt" + f;
    }

    // ------------------------------------------------------------------------

    private static void runCapture(int format, boolean maximumResolution, String outBase) {
        CameraDevice[] camHolder = new CameraDevice[1];
        ImageReader reader = null;
        try {
            reader = ImageReader.newInstance(WIDTH, HEIGHT, format, 2);
            final ImageReader r = reader;

            final CountDownLatch imageLatch = new CountDownLatch(1);
            final String[] imageInfo = new String[1];

            r.setOnImageAvailableListener(new ImageReader.OnImageAvailableListener() {
                @Override
                public void onImageAvailable(ImageReader ir) {
                    Image img = null;
                    try {
                        img = ir.acquireNextImage();
                        if (img == null) {
                            log("onImageAvailable: acquireNextImage returned null");
                            return;
                        }
                        imageInfo[0] = saveImage(img, outBase);
                    } catch (Throwable t) {
                        log("image handling threw: " + t);
                        t.printStackTrace(System.out);
                    } finally {
                        if (img != null) img.close();
                        imageLatch.countDown();
                    }
                }
            }, handler);

            // -- open camera ---------------------------------------------------
            final CountDownLatch openLatch = new CountDownLatch(1);
            final Throwable[] openErr = new Throwable[1];
            cameraManager.openCamera(CAMERA_ID, new CameraDevice.StateCallback() {
                @Override public void onOpened(CameraDevice c) {
                    camHolder[0] = c; openLatch.countDown();
                }
                @Override public void onDisconnected(CameraDevice c) {
                    openErr[0] = new IllegalStateException("camera disconnected");
                    c.close(); openLatch.countDown();
                }
                @Override public void onError(CameraDevice c, int e) {
                    openErr[0] = new IllegalStateException("camera open error code " + e);
                    c.close(); openLatch.countDown();
                }
            }, handler);

            if (!openLatch.await(TIMEOUT_SEC, TimeUnit.SECONDS)) {
                log("TIMEOUT opening camera"); return;
            }
            if (openErr[0] != null) { log("OPEN FAILED: " + openErr[0]); return; }
            final CameraDevice cam = camHolder[0];
            log("camera opened: " + cam.getId());

            // -- configure session ---------------------------------------------
            // -- The stream must DECLARE which sensor pixel mode it will be used
            // in. Without this, the service rejects the request with
            //   "CONTROL_SENSOR_PIXEL_MODE are not consistent with streams
            //    configured"
            // because it infers {DEFAULT} from the size appearing in the default
            // stream map. This is the correct API for an ultra-high-resolution
            // sensor and is what makes the MAXIMUM_RESOLUTION request legal.
            OutputConfiguration oc = new OutputConfiguration(r.getSurface());
            if (maximumResolution) {
                oc.addSensorPixelModeUsed(
                    CameraMetadata.SENSOR_PIXEL_MODE_MAXIMUM_RESOLUTION);
                log("OutputConfiguration: addSensorPixelModeUsed(MAXIMUM_RESOLUTION)");
            } else {
                oc.addSensorPixelModeUsed(CameraMetadata.SENSOR_PIXEL_MODE_DEFAULT);
                log("OutputConfiguration: addSensorPixelModeUsed(DEFAULT)");
            }

            List<OutputConfiguration> outputs = new ArrayList<OutputConfiguration>();
            outputs.add(oc);

            Executor exec = new Executor() {
                @Override public void execute(Runnable cmd) { handler.post(cmd); }
            };

            final CountDownLatch sessLatch = new CountDownLatch(1);
            final CameraCaptureSession[] sessHolder = new CameraCaptureSession[1];
            final Throwable[] sessErr = new Throwable[1];

            SessionConfiguration sc = new SessionConfiguration(
                SessionConfiguration.SESSION_REGULAR, outputs, exec,
                new CameraCaptureSession.StateCallback() {
                    @Override public void onConfigured(CameraCaptureSession s) {
                        sessHolder[0] = s; sessLatch.countDown();
                    }
                    @Override public void onConfigureFailed(CameraCaptureSession s) {
                        sessErr[0] = new IllegalStateException(
                            "session CONFIGURE FAILED at " + WIDTH + "x" + HEIGHT);
                        sessLatch.countDown();
                    }
                });

            try {
                log("isSessionConfigurationSupported: "
                    + cam.isSessionConfigurationSupported(sc));
            } catch (Throwable t) {
                log("isSessionConfigurationSupported threw: " + t);
            }

            cam.createCaptureSession(sc);

            if (!sessLatch.await(TIMEOUT_SEC, TimeUnit.SECONDS)) {
                log("TIMEOUT configuring session"); return;
            }
            if (sessErr[0] != null) {
                log("SESSION FAILED: " + sessErr[0]);
                log("  (a configuration failure at max-res is itself a result: it "
                    + "means the framework will not accept this geometry, most "
                    + "likely because the d0015/d0016 duration tables are empty)");
                return;
            }
            CameraCaptureSession session = sessHolder[0];
            log("session configured");

            // -- build the request ---------------------------------------------
            CaptureRequest.Builder b = cam.createCaptureRequest(CameraDevice.TEMPLATE_STILL_CAPTURE);
            b.addTarget(r.getSurface());
            if (maximumResolution) {
                b.set(CaptureRequest.SENSOR_PIXEL_MODE,
                      CameraMetadata.SENSOR_PIXEL_MODE_MAXIMUM_RESOLUTION);
                log("request: SENSOR_PIXEL_MODE = MAXIMUM_RESOLUTION ("
                    + CameraMetadata.SENSOR_PIXEL_MODE_MAXIMUM_RESOLUTION + ")");
            } else {
                log("request: SENSOR_PIXEL_MODE left DEFAULT (key not set)");
            }
            log("request readback SENSOR_PIXEL_MODE: " + b.get(CaptureRequest.SENSOR_PIXEL_MODE));

            final CountDownLatch resultLatch = new CountDownLatch(1);
            session.capture(b.build(), new CameraCaptureSession.CaptureCallback() {
                @Override
                public void onCaptureCompleted(CameraCaptureSession s,
                                               CaptureRequest req,
                                               TotalCaptureResult res) {
                    log("--- RESULT METADATA ---");
                    Integer pm = res.get(CaptureResult.SENSOR_PIXEL_MODE);
                    log("  SENSOR_PIXEL_MODE            : " + pm + " ("
                        + (pm == null ? "null"
                           : pm == CameraMetadata.SENSOR_PIXEL_MODE_MAXIMUM_RESOLUTION
                             ? "MAXIMUM_RESOLUTION" : "DEFAULT") + ")");
                    log("  SENSOR_RAW_BINNING_FACTOR_USED: "
                        + res.get(CaptureResult.SENSOR_RAW_BINNING_FACTOR_USED));
                    log("  SCALER_CROP_REGION            : "
                        + res.get(CaptureResult.SCALER_CROP_REGION));
                    log("  SENSOR_TIMESTAMP              : "
                        + res.get(CaptureResult.SENSOR_TIMESTAMP));
                    resultLatch.countDown();
                }
                @Override
                public void onCaptureFailed(CameraCaptureSession s,
                                            CaptureRequest req,
                                            android.hardware.camera2.CaptureFailure f) {
                    log("CAPTURE FAILED: reason=" + f.getReason()
                        + " wasImageCaptured=" + f.wasImageCaptured());
                    resultLatch.countDown();
                }
            }, handler);

            if (!resultLatch.await(TIMEOUT_SEC, TimeUnit.SECONDS)) {
                log("TIMEOUT waiting for capture result");
            }
            if (!imageLatch.await(TIMEOUT_SEC, TimeUnit.SECONDS)) {
                log("TIMEOUT waiting for image");
            } else {
                log("saved: " + imageInfo[0]);
            }

            session.close();
        } catch (Throwable t) {
            log("runCapture threw: " + t);
            t.printStackTrace(System.out);
        } finally {
            if (camHolder[0] != null) camHolder[0].close();
            if (reader != null) reader.close();
            try { Thread.sleep(1500); } catch (InterruptedException ignored) { }
        }
    }

    /**
     * Saves plane 0 verbatim and reports the geometry that the fold was
     * originally diagnosed from. rowStride is printed explicitly and is encoded
     * into the filename so the measuring script cannot guess it wrong.
     */
    private static String saveImage(Image img, String outBase) throws Exception {
        int w = img.getWidth();
        int h = img.getHeight();
        int fmt = img.getFormat();
        Image.Plane p = img.getPlanes()[0];
        ByteBuffer buf = p.getBuffer();
        int rowStride = p.getRowStride();
        int pixelStride = p.getPixelStride();
        int remaining = buf.remaining();

        log("--- IMAGE GEOMETRY ---");
        log("  width x height : " + w + " x " + h);
        log("  format         : " + fmtName(fmt) + " (0x" + Integer.toHexString(fmt) + ")");
        log("  rowStride      : " + rowStride);
        log("  pixelStride    : " + pixelStride);
        log("  planes         : " + img.getPlanes().length);
        log("  buffer bytes   : " + remaining);
        log("  implied rows   : " + (rowStride > 0 ? (remaining / rowStride) : -1));

        byte[] data = new byte[remaining];
        buf.get(data);

        String path = outBase + "_" + w + "x" + h
                    + "_stride" + rowStride
                    + "_ps" + pixelStride
                    + "_" + fmtName(fmt) + ".raw";
        FileOutputStream fos = new FileOutputStream(path);
        fos.write(data);
        fos.close();
        log("  wrote          : " + path + " (" + data.length + " bytes)");
        return path;
    }
}
