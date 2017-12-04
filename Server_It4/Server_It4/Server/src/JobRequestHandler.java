import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.InvalidPathException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
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

	int JobCode;

	// Numbered jobs that this device has direct control of.
	static final int JOB_1 = 1;		// i.e. run DC motor
	static final int JOB_2 = 2;		// i.e. LED pattern and signal interval to arduino, then execute
						// After jrqResponseHandler finishes main loop to write pattern, check: if job 2, execute arduino program in seperate method.

	/*TFTP DC motor job request
	 * Setup for initial job request
	1. write 0 to RPS.txt
	2. execute runDC.py

	Back to jrqResponseHandler to handle user inputs.
	3. poll for user input and then write it to RPS.txt
	4. the runDC.py will read the value from RPS.txt and calculate the duty cycle to apply, loops constantly reading the file.
	5. When TFTP connection severed by sending an empty data field, write -1 to RPS so runDC.py breaks loop and ends.
	*/

	InetAddress remoteIpAddress;
	int remotePort;

	int expectedBlock;

	//file streams
	FileOutputStream fileOutputStream;
	BufferedOutputStream bufferedOutputStream;



    // Within job  request packet
	// 2 bytes | 2 bytes |
	// Opcode  | Job code|

	// After request use data packet to transfer user input.

	public JobRequestHandler(ReceivedPacketHandler rcvHdl){

		rcvHanlder = rcvHdl;

		// of course max byte of 516 is too much, we expect less/equal than 6 bytes.
		dataBuf = new byte[maxByte];
		sendBuf = new byte[maxByte];

		extraBuf = new byte[518];			// extra bytes to test too long packet

		pkg = rcvHanlder.receivedPacket;
		expectedBlock = 0;
	}

	public void jrqResponseHandler() {

		try {

			if(processFirstPackage()) {
				// After job request, waits a timeout period
				int numPrevBlockReceived = 0;

				while(rcvHanlder.continueRun) {
					DatagramPacket packet = new DatagramPacket(extraBuf, extraBuf.length);
					//It_3. Network error starts

					try {
						if(JobCode == 1){	// Longer time out for DC motor inputs since user controlled, say 10 seconds of inactivity , close socket
							rcvHanlder.transferSocket.setSoTimeout(10000);
							rcvHanlder.transferSocket.receive(packet);
						}
						if(JobCode == 2){ //Stream of data for job 2.
							rcvHanlder.transferSocket.setSoTimeout(5000);
							rcvHanlder.transferSocket.receive(packet);
						}

						if(packet.getLength() > maxByte){

							//error, illegal TFTP operation

							ErrorMessagesHandler invHld = new ErrorMessagesHandler(rcvHanlder);
							invHld.errorHandler(ErrorMessagesHandler.RFC_ILLEGAL_OP, ErrorMessagesHandler.PACKET_LONGER_THAN_516);

							System.out.printf("Expected Packet to be 516 bytes, but received greater than 516 bytes", packet.getLength());

							continue;
						}
					} catch (SocketTimeoutException ex) {

						//Wait for the package for 5 second. Long enough, quit.
						System.out.println("WRQ: Timedout! " + ex.getMessage() + ". File incomplete.");

						closeBufferedOutputStream();
						closeFileOutputStream();

						// Not deleting the file if incomplete transfer since executing the the LED program will use the same file.
						// Just the data will be overwritten in the next request.
						//if(new File(strgFileName).delete()){
						//	System.out.println("\nIncomplete file deleted:" + strgFileName);
						//} else {
						//	System.out.println("\nFailed to delete incomplete file.");
						//}

			        	break;
					}


				InetAddress incomingIpAddress = packet.getAddress();
		        	int incomingPort = packet.getPort();

		        	// Checks incoming packet address and port.
		        	if((remotePort != incomingPort) || !(remoteIpAddress.equals(incomingIpAddress))){
		        		// Send error message back to the remote wrong port using information for the wrong packet
		        		ErrorMessagesHandler invHld = new ErrorMessagesHandler(rcvHanlder, packet);
		    			invHld.errorHandler(ErrorMessagesHandler.RFC_UNKNOWN_TID, ErrorMessagesHandler.UNKNOWNTID_INDEX);
		        		continue;
		        	}


		        	receivedPackageDataLen = packet.getLength();

		        	dataBuf = packet.getData();
		        	//Received an error code in the opcode section
		        	if(rcvHanlder.isErrorPackage(dataBuf)){
						int errorCode = rcvHanlder.getErrorCode(dataBuf);

						// get error code.
						if(errorCode == 5){
							rcvHanlder.printContents(packet);
							System.out.println("\n Server has received Error Packet, Unkown TID, and will now shutdown this thread. See messaage above.");
						}
						else if(errorCode == 4){
							rcvHanlder.printContents(packet);
							System.out.println("\n Server has received Error Packet, Illegal TFTP operation, and will now shutdown this thread. See messaage above.");

						} else {
							rcvHanlder.printContents(packet);
							System.out.println("\n Server has received Error Packet and will now shutdown this thread. See messaage above.");
						}
						closeBufferedOutputStream();
		    			closeFileOutputStream();
		    			break;
		        	}

		        	int curBlock = rcvHanlder.getPkgBlock(dataBuf);

		        	//It_3. Network error starts
		        	if(curBlock < expectedBlock) {
		        		//Network error. This package block # is the same as a previous block #. Client must be re-sending.
		        		//Server has already received the package because server block # has increased. Don't need to save data into file.
		        		//Re-send ACK to client, then go back to beginning of while loop.
		        		//If this happens up to 3 times consecutively, time to quit?.
		        		//This is checked by incrementing numPrevBlockReceived every time get in here. Clear numPrevBlockReceived after every good package.

		        		sendBuf[0] = 0;		//ack
			        	sendBuf[1] = 4;		//ack
			        	sendBuf[2] = dataBuf[2];
			        	sendBuf[3] = dataBuf[3];
			        	sendLen = 4;

		        		packet = new DatagramPacket(sendBuf, sendLen, remoteIpAddress, remotePort);
			        	rcvHanlder.transferSocket.send(packet);

			        	numPrevBlockReceived++;
			        	System.out.println("WRR:          Previous block # received " + numPrevBlockReceived + " times. Re-sent ACK back to client.");
			        	if(numPrevBlockReceived >= 3) {
			        		//consecutively received previous block number 3 times. Give up and quit.
			    			closeBufferedOutputStream();
			    			closeFileOutputStream();
			        		break;
			        	}
		        	}
		        	//It_3. Network error end. Go back to beginning of while loop

		        	else {

			        	if(curBlock > expectedBlock) {
			    			ErrorMessagesHandler invHld = new ErrorMessagesHandler(rcvHanlder);
			    			invHld.errorHandler(ErrorMessagesHandler.RFC_ILLEGAL_OP, ErrorMessagesHandler.INVLIAD_WR_BLOCK, expectedBlock, curBlock);
			    			closeBufferedOutputStream();
			    			closeFileOutputStream();
				        	break;
			        }
			        //correct
		        	numPrevBlockReceived = 0;
		        	receivedPackageDataLen = packet.getLength();
		        	System.out.println("JRQ: Received OpCode:" + rcvHanlder.getPkgOpCode(dataBuf) + ", Block:" + curBlock + ", Packet Length:" + receivedPackageDataLen);
			        System.out.println("JRQ:          Local port(Host TID):" + rcvHanlder.transferSocket.getLocalPort() + " local IP: " + rcvHanlder.transferSocket.getLocalAddress());
			        System.out.println("JRQ:          remote port(remote TID):" + packet.getPort() + ", remote IP: " + packet.getAddress());

			        rcvHanlder.printContents(packet);

		        	//write to file the contents of the data packet
			        byte[] wrBuf = Arrays.copyOfRange(dataBuf, 4, receivedPackageDataLen);
			        Boolean wrResultOk = WriteToFile(wrBuf, receivedPackageDataLen -4);
		        	if(!wrResultOk) {
		    			closeBufferedOutputStream();
		    			closeFileOutputStream();
		    			System.out.println("Could not write to " + strgFileName);
			        	break;
		        	}


			        	//ACK cmd
			        	sendBuf[0] = 0;		//ack
			        	sendBuf[1] = 4;		//ack
			        	sendBuf[2] = dataBuf[2];
			        	sendBuf[3] = dataBuf[3];
			        	sendLen = 4;

			        	packet = new DatagramPacket(sendBuf, sendLen, remoteIpAddress, remotePort);
			        	rcvHanlder.transferSocket.send(packet);
			        	System.out.println("\nWRR:          Sent ACK back to client. OpCode: 04, Block: " + rcvHanlder.getPkgBlock(sendBuf)+"\n");

				        expectedBlock = curBlock + 1;

					// This section checks if it was the final packet or not.
					/*if(JobCode == 1){
				        // empty data bytes, then quit this is for job 1
						if(receivedPackageDataLen == 4) {
							//done
							// No value in the data packet to write, so it indicates the user is done.
							bufferedOutputStream.flush();
							closeBufferedOutputStream();
							closeFileOutputStream();
							try {
									TimeUnit.SECONDS.sleep(1);

								} catch (InterruptedException e) {
									e.printStackTrace();
								}

							// write -1 to RPS.txt so runDC.py breaks its loop and ends properly.
							byte[] end = new byte[] {-1};
							Boolean ending = WriteToFile(end, 2);
							System.out.println("End value written to RPS.txt: " + ending);

							//break loop that waits for user input before long time out.
							break;
						}
					}*/

					//if(JobCode == 2){
						if(receivedPackageDataLen < 516) {
							//done

							bufferedOutputStream.flush();
							closeBufferedOutputStream();
							closeFileOutputStream();
							try {
									TimeUnit.SECONDS.sleep(1);

								} catch (InterruptedException e) {
									e.printStackTrace();
								}

							// Call function to execute LED program for Arduino.




							}
						break;
			        //}


					/*
					4. the runDC.py will read the value from RPS.txt and calculate the duty cycle to apply, loops constantly reading the file.
					5. When TFTP connection severed by sending an empty data field, write -1 to RPS so runDC.py breaks loop and ends.
					*/


				}

			}
			}

		} catch (IOException e) {
			e.printStackTrace();
		}
		finally {
			System.out.println("WRR: ----------Write Request, completed. Socket closed.");
			rcvHanlder.transferSocket.close();
		}

	}

	// First package processing for packet information
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
			JobCode = getJobCode(dataBuf);

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
					jobDONE = false;
					break;

			}


			if(jobDONE){
				//send ACK packet if the setup for the job was successful

				sendBuf[0] = 0;	//ACK high byte
				sendBuf[1] = 4;	//ACK low byte
				sendBuf[2] = (byte)(expectedBlock >> 8);	//block high byte
				sendBuf[3] = (byte)(expectedBlock);			//block 0 low byte
				sendLen = 4;

	        	//sends the ACK packet.
				DatagramPacket packet = new DatagramPacket(sendBuf, sendLen, remoteIpAddress, remotePort);
				rcvHanlder.transferSocket.send(packet);
				System.out.println("JRQ: local port(Host TID):" + rcvHanlder.transferSocket.getLocalPort() + ", remote port(remote TID):" + packet.getPort());

				expectedBlock += 1;

				result = true;

				//---------
				// continue connection

				//expectedBlock += 1;

				//-- close when client sends a special packet or timeout
				//rcvHanlder.transferSocket.close();

			} else {
				result = false;
			}

		}
		catch (Exception ex) {
			ex.printStackTrace();
		}

		return result;
	}

	public int getJobCode(byte[] b){

		return ((b[2] << 8) & 0xff00) + (b[3] & 0xff);

	}



	private boolean doJob1(){
		/*TFTP DC motor job request
		 * Setup for initial job request
1. write 0 to RPS.txt
2. execute runDC.py\\

Back to jrqResponseHandler to handle user inputs.
3. poll for user input and then write it to RPS.txt
4. the runDC.py will read the value from RPS.txt and calculate the duty cycle to apply, loops constantly reading the file.
5. When TFTP connection severed by sending an empty data field, write -1 to RPS so runDC.py breaks loop and ends.
*/
		// 1. Check if RPS.txt file exists or created. Write 0 to RPS.txt

		//tests
		String RPSfile = "C:\\Users\\Jonathan\\Documents\\LED_Globe\\Server_It4\\testRPSfile.txt";  // Test file to write to
		String DCpy = "C:\\Users\\Jonathan\\Documents\\LED_Globe\\Server_It4\\runDCfake.py";        // Test file to execute

		// actual
		//String RPSfile = "/home/Desktop/RPS.txt";
		//String DCpy = "/home/Desktop/runDC.py";

		File f = new File(DCpy);

		boolean result = false;

		if (filePresent(RPSfile, true) && f.exists()) {
			// write 0 to RPS.txt to reset it to this default value and also to test write to this file.
			byte[] wrBuf = new byte[] {0};
			if(WriteToFile(wrBuf, 1)) {

				//2. execute runDC.py through command line on the RPi
				// If able, then send ACK and wait for user inputs.

				// Problem here
				if(runDC(DCpy)) {

					// Job request setup complete. Ready to receive user input.
					// back to jrqResponseHandler()

					result = true;


				} else {
					// execution of py file failed.
					System.out.format("%s has failed to execute, see error message above.", DCpy);
					result = false;
				}
			} else {
				System.out.println(RPSfile + " could not be writen to.");
				result = false;
			}

		} else {
			// fail RPS check and runDC.py
			System.out.println("Either /home/Desktop/RPS.txt and/or /home/Desktop/runDC.py has encountered a problem. See error message above.");
			result = false;
		}

		return result;
	}

  // 1. Store LED pattern in a text file and the delay time in another textfile.
  // 2. Load Arduino sketch program that controls the LEDs on the ring with the 2 text files.
  // Incomplete.
	private boolean doJob2() {
		String ledFile = "C:\\Users\\Jonathan\\Documents\\LED_Globe\\Server_It4\\Write_testLEDpattern.txt";   //Test file to write to
    String signalFile = "C:\\Users\\Jonathan\\Documents\\LED_Globe\\Server_It4\\Write_testSignalfile.txt";//Test file to write to
		boolean result = false;

		if (filePresent(ledFile, true) && filePresent(signalFile, true)) {

			result = true;
		}

		return result;

	}

	// check if file exists, if not create.
	private boolean filePresent(String fileNM, boolean create) {
		Boolean result = false;
		strgFileName = fileNM;
		try {

			File file = new File(strgFileName);

			if (file.exists()) {

				fileOutputStream = new FileOutputStream(file, false);	//false means overwrite
				bufferedOutputStream = new BufferedOutputStream(fileOutputStream);
				result = true;

			}
			else if (!file.exists() && create){
				// create new file with the name
				result = file.createNewFile();	//should equal true if created properly
				fileOutputStream = new FileOutputStream(file, false);	//false means overwrite
				bufferedOutputStream = new BufferedOutputStream(fileOutputStream);
				//result = true;
			}
		}
		catch (IOException ex) {	//create
			//Iteration #4
			//ErrorMessagesHandler invHld = new ErrorMessagesHandler(rcvHanlder);
			//invHld.errorHandler(ErrorMessagesHandler.RFC_ACCESS_VIOLATION, ErrorMessagesHandler.FILE_CREATE_FAILED, strgFileName);
			System.out.println("Error regarding " + strgFileName + ":" + ex.toString());
			result = false;
		}


		System.out.format("File exists %s result: %s\n", strgFileName, result.toString());
		return result;
	}

	private boolean WriteToFile(byte[] b, int len) {
		boolean result = false;
		try {
			// opened file is RPS.txt
			bufferedOutputStream.write(b, 0, len);


			result = true;

		} catch (IOException e) {
			//Iteration #4
			ErrorMessagesHandler invHld = new ErrorMessagesHandler(rcvHanlder);
			invHld.errorHandler(ErrorMessagesHandler.RFC_DISK_FULL, ErrorMessagesHandler.WRITE_FAILED, strgFileName);
			result = false;
		}
		return result;
	}

	private boolean runDC(String pyFile) {

		String command = "python " + pyFile;

		try {

			//execute in command line, string for pyfile may need to be changed depending to starting directory?
			Process p = Runtime.getRuntime().exec(command);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			System.out.println("WRQ: Failed to execute " + command + ":" + e.getMessage());
			return false;
		}

		return true;

	}

	void closeBufferedOutputStream() {
		if(bufferedOutputStream!=null) {
			try {
				bufferedOutputStream.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	void closeFileOutputStream() {
		if(fileOutputStream!=null) {
			try {
				fileOutputStream.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
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
