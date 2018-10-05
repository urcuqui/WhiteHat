package udp;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class NewsUDPClient {

	private final static int PORT = 9000;
	private final static String HOSTNAME = "localhost";
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		// the next line specifies that the client is going to have the port 0
				try {
					DatagramSocket socket = new DatagramSocket(9);
					socket.setSoTimeout(10000);
					InetAddress host = InetAddress.getByName(HOSTNAME);
					// these are the request and response packages
					DatagramPacket request =  new DatagramPacket(new byte[1], 1, host, PORT);
					DatagramPacket response = new DatagramPacket(new byte[1024], 1024);
					// we are going to get and send the package through the socket previously made, it is only a package that allows us to start the communication
					socket.send(request);
					// we are going to process each answer from the server
					while(true)
					{
						socket.receive(response);
						String result = new String(response.getData(), 0, response.getLength(), "US-ASCII");
						System.out.println(result);	
					}
					
				} catch (SocketException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (UnknownHostException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					System.err.println("Could not connect to server");
				}
	}

}
