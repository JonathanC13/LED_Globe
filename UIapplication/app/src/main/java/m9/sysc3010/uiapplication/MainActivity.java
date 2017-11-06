package m9.sysc3010.uiapplication;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    /*Method to send the request to start the Globe*/
    public void sendStartRequest(View view) {
        // Do something in response to Start button
    }

    /*Method to send the request to stop the Globe*/
    public void sendStopRequest(View view) {
        // Do something in response to Stop button
    }

    /*Method to send the user input to the Rpi*/
    public void sendInput(View view) {
        // Do something in response to Stop button
    }
}
