package m9.sysc3010.uiapplication;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {

    /*Method to send the request to stop the Globe*/
    public void sendStopRequest(View view) {
        // TODO place holer for stop button handler
    }

    /*Method to send the user input to the Rpi*/
    public void sendInput(View view) {
        // TODO place holder for user input button handler
    }


    BluetoothSocket mmSocket;
    BluetoothDevice mmDevice = null;

    // Delimiter will be "!" character
    final byte delimiter = 33;
    int readBufferPosition = 0;


    // Method to create Bluetooth socket, connect to server script, and send command.
    public void sendBtMsg(String msg2send){

        // This is a specific UUID known by the Bluetooth service script running on the RPi. Must
        // be the known on both sides to connect.
        UUID uuid = UUID.fromString("7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d");

        try {

            mmSocket = mmDevice.createRfcommSocketToServiceRecord(uuid);
            if (!mmSocket.isConnected()){
                mmSocket.connect();
            }

            OutputStream mmOutputStream = mmSocket.getOutputStream();
            mmOutputStream.write(msg2send.getBytes());

        } catch (IOException e) {
            // TODO Auto-generated catch block, must implement graceful handling
            e.printStackTrace();
        }

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Handler for making label thread safe (not needed so far since there's only
        // one thread for the one command implemented which is the "start" command).
        final Handler handler = new Handler();

        final TextView myLabel = (TextView) findViewById(R.id.btResult);
        final Button startButton = (Button) findViewById(R.id.button_start);

        BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        // In-class workerThread class definition to handle sending and
        // receiving across an RFComm channel. Could be in a separate file.
        final class workerThread implements Runnable {

            // Message we'll be sending for this thread.
            private String btMsg;

            // Construct the workerThread. The name of the thread is the Bluetooth command
            // we want to send to the server script.
            public workerThread(String msg) {
                btMsg = msg;
            }

            public void run()
            {
                // Send Bluetooth command message.
                sendBtMsg(btMsg);

                while(!Thread.currentThread().isInterrupted())
                {
                    int bytesAvailable;
                    boolean workDone = false;

                    try {

                        // Open the the input stream coming from the socket to receive response
                        // from the server script.
                        final InputStream mmInputStream;
                        mmInputStream = mmSocket.getInputStream();
                        bytesAvailable = mmInputStream.available();

                        if(bytesAvailable > 0)
                        {

                            // Reach here once there are bytes available to get from the input
                            // stream. Will read 1024 bytes into the buffer at a time.
                            byte[] packetBytes = new byte[bytesAvailable];
                            byte[] readBuffer = new byte[1024];
                            mmInputStream.read(packetBytes);

                            // Loop through the buffer to find the delimiter character.
                            for(int i=0;i<bytesAvailable;i++)
                            {
                                byte b = packetBytes[i];
                                if(b == delimiter)
                                {
                                    // Once delimiter is reached, all of the response from the
                                    // server is received, so extract buffer contents of buffer.
                                    byte[] encodedBytes = new byte[readBufferPosition];
                                    System.arraycopy(readBuffer, 0, encodedBytes, 0, encodedBytes.length);
                                    final String data = new String(encodedBytes, "US-ASCII");
                                    readBufferPosition = 0;

                                    // The variable data now contains our full response. Set the
                                    // label to output the response received from the server script.
                                    handler.post(new Runnable()
                                    {
                                        public void run()
                                        {
                                            myLabel.setText(data);
                                        }
                                    });

                                    workDone = true;
                                    break;

                                }

                                // If buffer doesn't contain the delimiter, continue reading from
                                // input stream.
                                else
                                {
                                    readBuffer[readBufferPosition++] = b;
                                }
                            } // End of for loop.

                            // Once full response is received from the server script, close the
                            // RFComm socket.
                            if (workDone == true){
                                mmSocket.close();
                                break;
                            }
                        } // End of if.

                    } catch (IOException e) {
                        // TODO Auto-generated catch block, must implement graceful handling
                        e.printStackTrace();
                    }

                } // End of while loop.
            }// End of run().

        } // End of class definition.

        // Start button handler
        startButton.setOnClickListener(new View.OnClickListener() {

            // Perform action on start button click
            public void onClick(View v) {

                // Start a new worker thread to handle the Bluetooth communication link
                // corresponding to the start request.
                Thread startButtonThread = new Thread(new workerThread("start"));
                startButtonThread.start();

                // Once user starts Globe, the start button will be unclickable. Must enable in
                // click handling for "end button".
                startButton.setEnabled(false);

            }
        });// End of start button handler

        // Get user to enable Bluetooth access for app if not already enabled
        if(!mBluetoothAdapter.isEnabled())
        {
            // Small intent to request user action
            Intent enableBluetooth = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBluetooth, 0);
        }

        // Get all paired devices
        Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
        if(pairedDevices.size() > 0)
        {
            // Find the RPi running the server script from the list of paired devices.
            for(BluetoothDevice device : pairedDevices)
            {
                if(device.getName().equals("RPI_Carleton"))
                {
                    mmDevice = device;
                    break;
                }
            }
        }


    }

}
