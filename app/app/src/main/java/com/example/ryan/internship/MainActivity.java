package com.example.ryan.internship;

import android.app.Activity;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Vibrator;
import android.util.Log;
import android.widget.TextView;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.time.*;

public class MainActivity extends Activity {
    private static final int EVENT_MEAN_COUNT = 100;
    private static final float RATE_OF_CHANGE = 0.2f;

    private static final int MAX_LIMIT = 1000;
    private static final int MIN_LIMIT = -1000;

    private SensorManager sensorManager;
    private SensorData sensorInstance;
    private PrintWriter logger;

    private Events events;
    private float[] means;
    private float[] standard_deviations;

    public int currentEvent;
    public int currentAccuracy;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        this.sensorManager = (SensorManager)getSystemService(SENSOR_SERVICE);
        this.sensorInstance = new SensorData();

        try {
            this.logger = new SocketSetup().execute().get(500, TimeUnit.MILLISECONDS);
        } catch (ExecutionException|InterruptedException|TimeoutException e) {
            this.logger = null;
        }

        this.events = new Events();

        this.currentEvent = 0;
        this.means = new float[] {0, 0, 0};
        this.standard_deviations = new float[] {0, 0, 0};

        setContentView(R.layout.activity_main);
    }

    @Override
    protected void onResume() {
        super.onResume();
        this.sensorInstance.start();
    }

    @Override
    protected void onPause() {
        super.onPause();
        this.sensorInstance.stop();
    }

    class SensorData implements SensorEventListener {
        private Sensor magneticFieldSensor;
        private Sensor accelerometerSensor;
        private Sensor gyroscopeSensor;
        private Sensor gravitySensor;

        private SensorData() {
            this.magneticFieldSensor = sensorManager.getDefaultSensor(
                    Sensor.TYPE_MAGNETIC_FIELD);
            this.accelerometerSensor = sensorManager.getDefaultSensor(
                    Sensor.TYPE_ACCELEROMETER);
            this.gyroscopeSensor = sensorManager.getDefaultSensor(
                    Sensor.TYPE_GYROSCOPE);
            this.gravitySensor = sensorManager.getDefaultSensor(
                    Sensor.TYPE_GRAVITY);
        }

        public void start() {
            // Enable the sensor when the activity is started, refreshing every 10ms.
            sensorManager.registerListener(this,  magneticFieldSensor, 10000);
            sensorManager.registerListener(this, accelerometerSensor, 10000);
            sensorManager.registerListener(this, gyroscopeSensor, 10000);
            sensorManager.registerListener(this, gravitySensor, 10000);
        }

        private void stop() {
            // Turn the sensor off when the activity is paused.
            sensorManager.unregisterListener(this);
        }

        public void onSensorChanged(SensorEvent event) {
            // When the sensor changes, react to the event it gives us.
            // That is, set the current text to this value, as well as altering the
            // text colour depending on the value of the event.


            if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {

                float currentAccXValue = event.values[0];
                float currentAccYValue = event.values[1];
                float currentAccZValue = event.values[2];

                events.xEvents.add(currentAccXValue);
                events.yEvents.add(currentAccYValue);
                events.zEvents.add(currentAccZValue);
                currentEvent = currentEvent + 1;

                if (currentEvent == EVENT_MEAN_COUNT - 1) {
                    this.getMeans();
                    this.getStandardDeviations();
                } else if (currentEvent % (EVENT_MEAN_COUNT * 15)== 0) {
                    this.updateMeans();
                    this.updateDeviations();
                }

                if (logger != null) {
                    String timeStampMillis = Long.toString(System.currentTimeMillis());
                    new LoggingUtil(logger).execute(
                            "EpochTime", timeStampMillis,
                            "AccX", String.format(Locale.getDefault(), "%.3f", currentAccXValue),
                            "AccY", String.format(Locale.getDefault(), "%.3f", currentAccYValue),
                            "AccZ", String.format(Locale.getDefault(), "%.3f", currentAccZValue)
                    );
                } else {
                    TextView apiLabel = findViewById(R.id.apiText);
                    apiLabel.setTextColor(getResources().getColor(R.color.black));
                }
            }

            if (event.sensor.getType() == Sensor.TYPE_GRAVITY) {

                float currentGravXValue = event.values[0];
                float currentGravYValue = event.values[1];
                float currentGravZValue = event.values[2];

                events.xEvents.add(currentGravXValue);
                events.yEvents.add(currentGravYValue);
                events.zEvents.add(currentGravZValue);
                currentEvent = currentEvent + 1;

                if (currentEvent == EVENT_MEAN_COUNT - 1) {
                    this.getMeans();
                    this.getStandardDeviations();
                } else if (currentEvent % (EVENT_MEAN_COUNT * 15)== 0) {
                    this.updateMeans();
                    this.updateDeviations();
                }

                if (logger != null) {
                    String timeStampMillis = Long.toString(System.currentTimeMillis());
                    new LoggingUtil(logger).execute(
                            "EpochTime", timeStampMillis,
                            "GravX", String.format(Locale.getDefault(), "%.3f", currentGravXValue),
                            "GravY", String.format(Locale.getDefault(), "%.3f", currentGravYValue),
                            "GravZ", String.format(Locale.getDefault(), "%.3f", currentGravZValue)
                    );
                } else {
                    TextView apiLabel = findViewById(R.id.apiText);
                    apiLabel.setTextColor(getResources().getColor(R.color.black));
                }
            }
            if (currentAccuracy == 0) {
                currentAccuracy = event.accuracy;
                updateAccuracyText();
            }
        }

        private void setSensorText(
                TextView label,
                float currentValue,
                float mean,
                float deviation
        ) {
            label.setText(String.format(Locale.getDefault(), "%.3f", currentValue));

            boolean medianNotSet = Float.compare(Math.abs(mean), 0) == 0;
            boolean insideRange = (
                    (currentValue >= mean - (deviation * 10)) &&
                            (currentValue <= mean + (deviation * 10))
            );
            boolean outsideSafeRange = currentValue >= MAX_LIMIT || currentValue <= MIN_LIMIT;

            if (outsideSafeRange) {
                Vibrator vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
                vibrator.vibrate(10);
                label.setTextColor(getResources().getColor(R.color.danger));
            } else if (!medianNotSet && !insideRange){
                label.setTextColor(getResources().getColor(R.color.warning));
            } else {
                label.setTextColor(getResources().getColor(R.color.noWarning));
            }
        }

        public void onAccuracyChanged(Sensor sensor, int accuracy) {
            // Should we do anything if the accuracy changes?
            Log.d("ACCURACY", "Accuracy changed to " + accuracy);

            currentAccuracy = accuracy;
            this.updateAccuracyText();
        }

        private void updateAccuracyText() {
            TextView accuracyLabel = findViewById(R.id.accuracyLabel);

            if (currentAccuracy < 2) {
                accuracyLabel.setTextColor(getResources().getColor(R.color.black));
            } else {
                accuracyLabel.setTextColor(getResources().getColor(R.color.transparent));
            }
        }

        private void getMeans() {
            float eventSum = 0;
            float[] currentMeans = {0, 0, 0};

            for (int axis = 0; axis < 3; axis++) {
                for (float event : events.get(axis)) {
                    eventSum += event;
                }
                currentMeans[axis] = (1.0f / currentEvent) * eventSum;
                eventSum = 0;
            }

            means = currentMeans;
        }

        private void updateMeans() {
            float[] updatedMeans = {0f, 0f, 0f};

            for (int axis = 0; axis < 3; axis++) {
                float newEvent = events.get(axis).get(events.get(axis).size() - 1);
                updatedMeans[axis] = (1 - RATE_OF_CHANGE) * means[axis] + RATE_OF_CHANGE * newEvent;
            }

            means = updatedMeans;
        }

        private void getStandardDeviations() {
            float eventSum = 0;
            float[] currentDeviations = {0, 0, 0};

            for (int axis = 0; axis < 3; axis++) {
                for (float event : events.get(axis)) {
                    eventSum += Math.pow(event - means[axis], 2);
                }
                currentDeviations[axis] = (float)Math.sqrt(1.0f / currentEvent) * eventSum;
                eventSum = 0;
            }

            standard_deviations = currentDeviations;
        }

        private void updateDeviations() {
            float[] updatedDeviations = {0f, 0f, 0f};

            for (int axis = 0; axis < 3; axis++) {
                float newEvent = events.get(axis).get(events.get(axis).size() - 1);
                updatedDeviations[axis] = (float)Math.sqrt((
                        (1 - RATE_OF_CHANGE) * Math.pow(standard_deviations[axis], 2) +
                                RATE_OF_CHANGE * Math.pow(newEvent - means[axis], 2)
                ));
            }

            standard_deviations = updatedDeviations;
        }
    }

    static class LoggingUtil extends AsyncTask<String, Void, Void> {
        private PrintWriter loggingWriter;

        private LoggingUtil(PrintWriter logger) {
            this.loggingWriter = logger;
        }

        @Override
        protected Void doInBackground(String... args) {
            String toLog = String.format(
                    Locale.getDefault(),
                    "%s:%s;%s:%s;%s:%s;%s:%s",
                    args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]
            );
            logDataToServer(toLog);

            return null;
        }

        private void logDataToServer(String toLog) {
            try {
                this.loggingWriter.append(toLog).append("\n");
                this.loggingWriter.flush();
            } catch (NullPointerException e) {
                Log.d("LOGGING", "Null Pointer, toLog: " + toLog);
            }
        }
    }

    static class SocketSetup extends AsyncTask<Void, Void, PrintWriter> {
        private Socket loggingSocket = null;
        private PrintWriter loggingWriter = null;

        @Override
        protected PrintWriter doInBackground(Void... args) {
            try {
                this.loggingSocket = new Socket("192.168.137.1", 5006);
                this.loggingWriter = new PrintWriter(loggingSocket.getOutputStream());
            } catch (IOException e) {
                e.printStackTrace();
            }

            return this.loggingWriter;
        }
    }

    class Events {
        public List<Float> xEvents;
        public List<Float> yEvents;
        public List<Float> zEvents;

        private Events() {
            this.xEvents = new ArrayList<>();
            this.yEvents = new ArrayList<>();
            this.zEvents = new ArrayList<>();
        }

        public List<Float> get(int index) {
            switch (index) {
                case 0:
                    return xEvents;
                case 1:
                    return yEvents;
                case 2:
                    return zEvents;
                default:
                    throw new IndexOutOfBoundsException("Index not valid.");
            }
        }
    }
}
