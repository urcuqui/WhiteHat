package udp;
import java.io.*;
import java.net.*;
import java.util.logging.Logger;
public abstract class NewsUDPServer implements Runnable{

	private final int bufferSize; // in bytes
	private final int port;
	private final Logger logger = Logger.getLogger(NewsUDPServer.class.getCanonicalName());
	private volatile boolean isShutDown = false;
	
	public NewsUDPServer(int port, int bufferSize) {
		this.bufferSize = bufferSize;
		this.port = port;
		}
	
	public NewsUDPServer(int port) {
		this(port, 8192);
		}
	
	@Override
	public void run() {
		byte[] buffer = new byte[bufferSize];
		try (DatagramSocket socket = new DatagramSocket(port)) 
		{
		socket.setSoTimeout(10000); // check every 10 seconds for shutdown
		while (true) 
		{
			if (isShutDown) return;
			DatagramPacket incoming = new DatagramPacket(buffer, buffer.length);
			try {
			socket.receive(incoming);
			this.respond(socket, incoming);
			} catch (SocketTimeoutException ex) {
			if (isShutDown) return;
			} catch (IOException ex) {
				System.err.println(ex.getMessage());			
			}
		} // end while
		} catch (SocketException ex) {
			System.err.println("Could not bind to port: " + port);
		}
	}
	
	public abstract void respond(DatagramSocket socket, DatagramPacket request)
			throws IOException;
	public void shutDown() 
	{
		this.isShutDown = true;
	}
//	
//	public static void main(String[] args) {
//		// TODO Auto-generated method stub
//		try {
//			System.out.println("UDP Server Started ...");
//			
//			DatagramSocket serverSocket = new DatagramSocket(9003);
//			
//			byte[] buffer = new byte[2014];			
//			DatagramPacket request = new DatagramPacket(buffer, buffer.length);
//			while(true)
//			{
//				serverSocket.receive(request);
//				NewsServerThread threadClient = new NewsServerThread(request);
//				threadClient.start();
//			}
//			
//		} catch (SocketException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		} catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//		System.out.println("UDP Server Terminating");
//				
//	}

}
