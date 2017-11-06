package m9.sysc3010.uiapplication;

import android.os.AsyncTask;
import android.os.Handler;
import org.apache.commons.net.tftp.TFTPClient;

/**
 * Created by denischupin on 10/30/2017.
 * A class to create a TFTP Client from UI
 */

public class TftpClientATask extends AsyncTask<String,String,TFTPClient> {
    private static final String     COMMAND     = "shutdown -s"      ;
    private              TFTPClient  tcpClient                        ;
    private              Handler    mHandler                         ;
    private static final String     TAG         = "ShutdownAsyncTask";

    /**
     * TftpClientATask constructor with handler passed as argument. The UI is updated via handler.
     * In doInBackground(...) method, the handler is passed to TCPClient object.
     * @param mHandler Handler object that is retrieved from MainActivity class and passed to TCPClient
     *                 class for sending messages and updating UI.
     */
    public TftpClientATask(Handler mHandler){
        this.mHandler = mHandler;
    }
    /**
     * Overriden method from AsyncTask class. There the TCPClient object is created.
     * @param params From MainActivity class empty string is passed.
     * @return TCPClient object for closing it in onPostExecute method.
     */
    @Override
    protected TFTPClient doInBackground(String...params){
        return new TFTPClient();
    }
}
