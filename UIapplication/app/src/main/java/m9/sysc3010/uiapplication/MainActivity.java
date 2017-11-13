package m9.sysc3010.uiapplication;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    /*Method to send the request to start the Globe*/
    public void sendStartRequest(View view) {
        // Do something in response to Start button RPM 45, 0602 - 0601
        //Make other buttons visible after click of start
        Button stopButton=(Button) findViewById(R.id.button_stop);
        Button inputButton=(Button) findViewById(R.id.button_input);
        inputButton.setVisibility(View.VISIBLE);
        stopButton.setVisibility(View.VISIBLE);
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
