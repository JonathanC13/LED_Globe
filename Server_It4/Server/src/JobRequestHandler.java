import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.InvalidPathException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;

public class JobRequestHandler {
	
	int receivedPackageDataLen;
    int opCode;

	ReceivedPacketHandler rcvHanlder;
	printByteArray bytePrinter;
	
	byte[] dataBuf;
	int dataLen;
	byte[] sendBuf;
	int sendLen;
	DatagramPacket pkg;
	
	byte[] byteFileName;
	String strgFileName;
	
	byte[] extraBuf;
	
	static final int maxByte = 516;
	
	int fileNameLen, modeLen;
	
	// Numbered jobs that this device has direct control of.
	static final int JOB_1 = 1;		// i.e. turn on lights
	static final int JOB_2 = 2;		// i.e. turn on PC
	
	InetAddress remoteIpAddress;
	int remotePort;
	
    // Within job request packet
	// 2 bytes | 2 bytes | 0 to 512 bytes if needed. |
	// Opcode  | JobCode |
	// The job of interest could be on this device.
    // If this device is the leader device and does not have the job then it propagates the job to the followers.
    // If this is a follower device and the job request doesn't concern it, then for now do nothing. If completes the job sends back an ACK.
    
	public JobRequestHandler(ReceivedPacketHandler rcvHdl){
		
		rcvHanlder = rcvHdl;	
		
		dataBuf = new byte[maxByte];
		sendBuf = new byte[maxByte];	
		
		extraBuf = new byte[518];			// extra bytes to test too long packet
		
		pkg = rcvHanlder.receivedPacket;
		//expectedBlock = 0;
	}
	
	public void jrqResponseHandler() {
	
		try {
			if(processFirstPackage()) {
				// if a specific job needs more than the initial packet.
				//int numPrevBlockReceived = 0;
				
			}
			
		} catch (IOException e) {
			e.printStackTrace();
		}	
		finally {
			System.out.println("WRR: ----------Write Request, completed. Socket closed.");	
			rcvHanlder.transferSocket.close();
		}
		
	}
	
	Boolean processFirstPackage() throws IOException {
		Boolean result = false;
		
		try {
			//the IP address and port number on the remote host from which the datagram was received.
	        remoteIpAddress = pkg.getAddress();
			remotePort = pkg.getPort(); 	
			
			byte[] dataBuf = pkg.getData();
			//int requestDataLen = pkg.getLength();
			
			// Job packet
			// 2 bytes | 2 bytes | 
			// Opcode  | Job code| 	
			int JobCode = getJobCode(dataBuf);

			// Find out the behaviour of the web service transfer
			
			boolean jobDONE = false;
			//boolean receivedACK = false;
			
			// Somewhere to ACK
			switch(JobCode) {
			case JOB_1:
				jobDONE = doJob1();
				break;
			
			case JOB_2:
				jobDONE = doJob2();
				break;
				
			default:
				// if this is the leader device and the job code is not here, then propagate to follower devices.
				// if follower, do nothing
				//dataLen = pkg.getLength();
				
				//Propagate job request to follower(s).
				//DatagramPacket Prop = new DatagramPacket(dataBuf,dataLen, FOLLOWER IP, FOLLOWER PORT);
				//rcvHanlder.transferSocket.send(Prop);				
				//System.out.println("JRQ Propagation: local port(Host TID):" + rcvHanlder.transferSocket.getLocalPort() + ", remote port(remote TID):" + Prop.getPort());
				
				//Wait for a time for ACK, if no reply then follower didn't complete job.
				// Can add code for job here but could not complete and code for job not here. Multiple followers, mutli-thread needed.
				/*
				DatagramPacket packet = new DatagramPacket(extraBuf, extraBuf.length);
				byte[] dataFollow;
				try {
					rcvHanlder.transferSocket.setSoTimeout(5000);
					rcvHanlder.transferSocket.receive(packet);
					dataFollow = packet.getData();
					
					if(rcvHanlder.isAckPackage(dataFollow)){
						
						receivedACK = true;
						
					} else {
						receivedACK = false;
						//error
					}
				}
				catch (SocketTimeoutException ex) {
					
					//Wait for the package for 5 second. Long enough, quit.
					System.out.println("WRQ: Timedout! " + ex.getMessage() + ". Deleting incomplete file.");
					receivedACK = false;
					//
				}
				*/
				// need at least 1 ACK, boolean receivedACK = true if follower sends back an ACK meaning it completed the job
				
				//
				
			}	
			
			// Entering this 'if' means that the job was complete either from the leader or the follower. Send main ACK.
			if(jobDONE){
				//send ACK packet if the job has been done
				
				// ACK cmd with no block #
				//| 2 bytes |
				//| ack op  |
	        	sendBuf[0] = 0;		//ack
	        	sendBuf[1] = 4;		//ack
	        	//sendBuf[2] = dataBuf[2];
	        	//sendBuf[3] = dataBuf[3]; 
	        	sendLen = 2;
				
				DatagramPacket packet = new DatagramPacket(sendBuf, sendLen, remoteIpAddress, remotePort);			
				rcvHanlder.transferSocket.send(packet);				
				System.out.println("JRQ: local port(Host TID):" + rcvHanlder.transferSocket.getLocalPort() + ", remote port(remote TID):" + packet.getPort());

				
				//---------
				// continue connection
				
				//expectedBlock += 1;
				
				//-- close when client sends a special packet or timeout
				rcvHanlder.transferSocket.close();
				
			} else {
				// Leader nor follower had the job.
				// For now print error information: Requested job, jobs on this device.
			}
			
			// TO DO - if a job needs lots of information meaning more packets, block increase, etc, return a true so it continues in the handler.
			// Knowing the job before hand, can just hard code that it returns true.
			
		}
		catch (Exception ex) {
			ex.printStackTrace();
		}
		
		return result;
	}
	
	public int getJobCode(byte[] b){
		return ((b[3] << 8) & 0xff00) + (b[4] & 0xff);
		
	}
	
	
	
	private boolean doJob1(){
		/*TFTP DC motor job request
1. write 0 to RPS.txt
2. execute runDC.py
3. poll for user input and then write it to RPS.txt
4. the runDC.py will read the value from RPS.txt and calculate the duty cycle to apply, loops constantly reading the file.
5. When TFTP connection severed, write -1 to RPS so it breaks loop
8*/
		
		// if job is confirmed done somehow, then return true
		return true;
	}
	
	private boolean doJob2(){
		return true;
	}

	
	// test job directly.
	boolean doJob(int JobCode){
		
		switch(JobCode) {
		case JOB_1:
			return doJob1();
		
		case JOB_2:
			return doJob2();
			
		default:
				// if this is the leader device and the job code is not here, then propagate to follower devices.
			return false;
		}	
	
	}
	
}
