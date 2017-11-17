package mockClient;
import java.io.IOException;
import java.net.*;
import java.nio.file.Path;

public class MockClient {
	
	byte[] dataBuf;
	
	byte[] sendBuf;
	byte[] extraBuf;
	static final int maxByte = 516;
	static final int extra = 518;
	static final int remotePort = 69;
	
	DatagramSocket sendReceiveSocket;	// Socket for sending and receiving datagram packets
	DatagramPacket packet;
	
	private static InetAddress remoteIP;
	int receivedPackageDataLen;
	
	byte[] byteFileName;
	String strgFileName;
	Path filePath;
	
	int expectedBlock;

	public static void main(String[] args){
		System.out.print("Test Case 1: ");
		MockClient test1 = new MockClient();
		test1.mockClient(1,"LOCAL","end");
		System.out.println("Test Case 1 END -----");
		
		System.out.print("Test Case 2: ");
		MockClient test3 = new MockClient();
		test3.mockClient(2,"LOCAL","end");
		System.out.println("Test Case 2 END -----");
	}
	
	private void mockClient(int jobNumber, String ip, String fileTrans){
		
		strgFileName = fileTrans;
		
		sendBuf = new byte[maxByte];	
		extraBuf = new byte[extra];
		
		MockClient client = new MockClient();
		client.ConstructSocket();
		
		if(!validIP(ip)) {
			client.shutdown();
		}
		try {
			remoteIP = InetAddress.getByName(ip);
		} catch (UnknownHostException e1) {
			
			e1.printStackTrace();
		}
		
		switch(jobNumber) {
		case 1:
			// request
			sendBuf[0] = 0;	
			sendBuf[1] = 6;	
			sendBuf[2] = 0;
			sendBuf[3] = 1;
			
			packet = new DatagramPacket(sendBuf, sendBuf.length, remoteIP, remotePort);
			try {
				client.sendReceiveSocket.send(packet);
			} catch (IOException e) {
				
				e.printStackTrace();
			}	
			
			//Test case 1, end after first ack.
			if(fileTrans.equals("end")) {
				client.EndafterACK();
			} else {
				// data transfer
			}
			
		case 2:
			
			// request
			sendBuf[0] = 0;	
			sendBuf[1] = 6;	
			sendBuf[2] = 0;
			sendBuf[3] = 2;
			
			packet = new DatagramPacket(sendBuf, sendBuf.length, remoteIP, remotePort);
			try {
				client.sendReceiveSocket.send(packet);
			} catch (IOException e) {
				
				e.printStackTrace();
			}	
			
			//Test case 1, end after first ack.
			if(fileTrans.equals("end")) {
				client.EndafterACK();
			} else {
				// data transfer
			}
			
		default:
			client.shutdown();
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
			e.printStackTrace();
		}
		
		dataBuf = packetRe.getData();	
		
		if(packetRe.getLength() >= 4) {							
			int blk = getPkgBlock(dataBuf);
			int opCode = getPkgOpCode(dataBuf);
			if( isAckPackage(dataBuf) && (blk==expectedBlock) ) {
				receivedPackageDataLen = packetRe.getLength();
	        	System.out.println("Client: Received ACK OpCode:" + opCode + ", Block:" + blk + ", Packet Length:" + receivedPackageDataLen);
	        	System.out.println("From:          remote port(remote TID):" + packet.getPort() + ", remote IP: " + packet.getAddress());
			}
		}
		shutdown();
		
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
