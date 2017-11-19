package mockClient;
import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.*;
import java.nio.file.InvalidPathException;
import java.nio.file.Path;
import java.nio.file.Paths;

public class MockClient {
	
	byte[] dataBuf;
	
	byte[] sendBuf;
	byte[] extraBuf;
	static final int maxByte = 516;
	static final int extra = 518;
	static int remotePort = 69;
	
	DatagramSocket sendReceiveSocket;	// Socket for sending and receiving datagram packets
	DatagramPacket packet;
	
	private static InetAddress remoteIP;
	int receivedPackageDataLen;
	
	byte[] byteFileName;
	String strgFileName;
	Path filePath;
	
	boolean timeToBreak = false;
	
	BufferedInputStream bufferedInputStream = null;
    FileInputStream  fileInputStream= null;
    
    public Boolean continueRun = true;
	
    int sendLen;
	int expectedBlock;
	
	protected void MockClient(int jobNumber, String ip, String fileTrans){
		
		sendLen = 0;
		
		sendBuf = new byte[maxByte];	
		extraBuf = new byte[extra];
		strgFileName = fileTrans;
		
		//MockClient client = new MockClient();
		this.ConstructSocket();
		
		if(ip.equals("LOCAL")){
			try {
				remoteIP = InetAddress.getLocalHost();
			} catch (UnknownHostException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} else {
			shutdown();
		}
		
		//if(!validIP(ip)) {
		//	client.shutdown();
		//}
		
		switch(jobNumber) {
		case 1:
			// request
			sendBuf[0] = 0;	
			sendBuf[1] = 6;	
			sendBuf[2] = 0;
			sendBuf[3] = 1;
			
			System.out.print(remoteIP);
			packet = new DatagramPacket(sendBuf, sendBuf.length, remoteIP, remotePort);
			try {
				sendReceiveSocket.send(packet);
			} catch (IOException e) {
				
				e.printStackTrace();
			}	
			
			//Test case 1, end after first ack.
			if(fileTrans.equals("end")) {
				EndafterACK();
			} else {
				testOperation();
			}
			
		case 2:
			
			// request
			sendBuf[0] = 0;	
			sendBuf[1] = 6;	
			sendBuf[2] = 0;
			sendBuf[3] = 2;
			
			packet = new DatagramPacket(sendBuf, sendBuf.length, remoteIP, remotePort);
			try {
				sendReceiveSocket.send(packet);
			} catch (IOException e) {
				
				e.printStackTrace();
			}	
			
			//Test case 1, end after first ack.
			if(fileTrans.equals("end")) {
				EndafterACK();
			} else {
				testOperation();
			}
			
		default:
			shutdown();
		}
	}
	
	private void EndafterACK() {
		expectedBlock = 0;
	
		DatagramPacket packetRe = null;
		
		packetRe = new DatagramPacket(extraBuf, extraBuf.length);
		try {
			sendReceiveSocket.setSoTimeout(5000);
			sendReceiveSocket.receive(packetRe);
		} catch (IOException e) {
			System.out.print("No ack received.");
			e.printStackTrace();
		}
		
		dataBuf = packetRe.getData();	
		
		if(packetRe.getLength() >= 4) {							
			int blk = getPkgBlock(dataBuf);
			int opCode = getPkgOpCode(dataBuf);
			if( isAckPackage(dataBuf) && (blk==expectedBlock) ) {
				receivedPackageDataLen = packetRe.getLength();
	        	System.out.println("Client: Received ACK OpCode:" + opCode + ", Block:" + blk + ", Packet Length:" + receivedPackageDataLen);
	        	System.out.println("From:          remote port(remote TID):" + packetRe.getPort() + ", remote IP: " + packetRe.getAddress());
			}
		}
		shutdown();
		
	}
	
	private void testOperation() {
		
		
		while(continueRun) {
			DatagramPacket packetRe = null;
			try { // expecting ACK
				packetRe = new DatagramPacket(extraBuf, extraBuf.length);
				sendReceiveSocket.setSoTimeout(5000);
				sendReceiveSocket.receive(packetRe);
			
			} catch (SocketTimeoutException a) {
				
				System.out.print("Client time out.");
				break;
			} catch (IOException e) {
				e.printStackTrace();
				break;
			}
			remoteIP = packetRe.getAddress();
			remotePort = packetRe.getPort(); 
			
			dataBuf = packetRe.getData();
			
			if(packetRe.getLength() >= 4) {							
				int blk = getPkgBlock(dataBuf);
				int opCode = getPkgOpCode(dataBuf);
				if( isAckPackage(dataBuf) && (blk==expectedBlock) ) {
					// correct packet
					receivedPackageDataLen = packetRe.getLength();
		        	System.out.println("Client: Received ACK OpCode:" + opCode + ", Block:" + blk + ", Packet Length:" + receivedPackageDataLen);
		        	System.out.println("From:          remote port(remote TID):" + packetRe.getPort() + ", remote IP: " + packetRe.getAddress());
				} else {
					System.out.print("Incorrect packet received, opcode: " + opCode + ", Block: " + blk );
					shutdown();
				}
			} else {
				System.out.print("Invalid packet");
				shutdown();
			}
			int curBlock = getPkgBlock(dataBuf);
			
			if(timeToBreak) {

    			closeBufferedInputStream();
    			closeFileInputStream();		        		
    		    break;
	        }
			
			if(openFileStream()) {
			// load data to transfer
				sendLen = readfromFile(sendBuf);
			
				if(sendLen != -1) {
			        
		        	expectedBlock = curBlock + 1;	
			        sendBuf[0] = 0;		//data
			        sendBuf[1] = 3;		//data
			        sendBuf[2] = (byte)((expectedBlock >> 8) & 0xff);
			        sendBuf[3] = (byte)(expectedBlock & 0xff);
			        
			        System.out.println("WR: Send Block:" + expectedBlock + ", Data Length:" + sendLen);
			        
		        	packet = new DatagramPacket(sendBuf, sendLen + 4, remoteIP, remotePort);
		        	printContents(packet);
		        	try {
						sendReceiveSocket.send(packet);
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}	
		        	
		        } else {
	
	    			closeBufferedInputStream();
	    			closeFileInputStream();
		        	break;
		        }
			}
	        			        
        	if(sendLen < 512) {
        		//done
        		closeBufferedInputStream();
    			closeFileInputStream();
        		break;
        	}
			
			
		}
		
		shutdown();
	}
	
	Boolean openFileStream() {
		Boolean result = false;
	
		try {
			filePath = Paths.get(strgFileName);			
			File file = new File(strgFileName);
  
			fileInputStream = new FileInputStream(file);
			bufferedInputStream = new BufferedInputStream(fileInputStream);
			
			result = true;
		}
		catch(InvalidPathException | NullPointerException ex) {	//Paths.get() and new File()
			//Iteration #4
			System.out.println("RRQ: openFileStream. " + ex.getMessage());		
			
		}
		catch(FileNotFoundException ex) {	//FileInputStream
			//Iteration #4
			System.out.println("RRQ: openFileStream. " + ex.getMessage());			
			
		}
		catch(Exception ex) {
			//Iteration #4
			
			ex.printStackTrace();
		}
	
		System.out.format("Created an inpur (read) file %s result: %s\n", strgFileName, result.toString());
		return result;
	}

	
	// Create socket for sending and receiving
	private void ConstructSocket(){
		try{
			sendReceiveSocket = new DatagramSocket(); 	// Contruct a datagram socket and bind it to any available port on the local machine.
														// Used to send and receive UDP Datagram packets
            
		} catch (SocketException se){
			
			System.out.println("Contructing Socket failed: " + se.toString());
			se.printStackTrace();
			System.exit(1);
		}
	}
	private void shutdown() {
		
		sendReceiveSocket.close();			// unbind socket, blocks additional incoming requests
		System.out.println("Client port closed.");
		System.out.println("Client shutting down.");

		System.exit(0);
		
	}
	// Determine if input was a valid IP format.
		public static boolean validIP (String ip) {
		    try {
		    	
		        if ( ip == null || ip.isEmpty() ) {
		            return false;
		        }

		        String[] parts = ip.split( "\\." );
		        if ( parts.length != 4 ) {
		            return false;
		        }

		        for ( String s : parts ) {
		            int i = Integer.parseInt( s );
		            if ( (i < 0) || (i > 255) ) {
		                return false;
		            }
		        }
		        if ( ip.endsWith(".") ) {
		            return false;
		        }

		        return true;
		    } catch (NumberFormatException nfe) {
		        return false;
		    }
		}
		
		int readfromFile(byte[] buffer) {
			
			int read = -1;
			
			try {
				read = bufferedInputStream.read(buffer, 4, 512);
				
			} catch (IOException ex) {
	    		
				read = -1;
			}

			return read;
		}
		

		void closeBufferedInputStream() {
			try {
				if(bufferedInputStream!=null) {
					bufferedInputStream.close();
				}
			}
			catch (Exception ex) {
				ex.printStackTrace();
			}
		}
		
		void closeFileInputStream() {
			try {
				if(fileInputStream!=null) {
					fileInputStream.close();
				}
			}
			catch (Exception ex) {
				ex.printStackTrace();
			}
		}
		
		protected void printContents(DatagramPacket p){

		       
	        byte[] data = new byte[p.getLength()];
	        System.arraycopy(p.getData(), 0, data, 0, data.length);

	        System.out.print("Containing (String): \n");
	        String received = new String(p.getData(),0,p.getLength());   
	        System.out.println(received + "\n");

		}
		
		//opcode is the first two bytes in big endian
		public int getPkgOpCode(byte[] b) {
			return ((b[0] << 8) & 0xff00) + (b[1] & 0xff);
		}
		
		public Boolean isDataPackage(byte[] b) {
			return (getPkgOpCode(b) == 3);
		}	
		public Boolean isAckPackage(byte[] b) {
			return (getPkgOpCode(b) == 4);
		}	

		//opcode is the first two bytes in big endian
		public int getPkgBlock(byte[] b) {
			return ((b[2] << 8) & 0xff00) + (b[3] & 0xff);
		}
	
}
