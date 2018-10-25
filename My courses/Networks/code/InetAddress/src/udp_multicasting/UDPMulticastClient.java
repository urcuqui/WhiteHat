package udp_multicasting;

import java.io.IOException;
import java.net.*;

public class UDPMulticastClient {

	public UDPMulticastClient()
	{
		System.out.println("UDP Multicast Time Client Started");
		try 
		{
			/**
			 * We are going to make an InetAddress instance using the multicast address of 228.5.6.7.
			 * The client then joins the multicast group using the joinGroup method
			 */
			MulticastSocket multicastSocket = new MulticastSocket(9877);
			InetAddress inetAddress = InetAddress.getByName("228.5.6.7");
			multicastSocket.joinGroup(inetAddress);
			
			/**
			 * A DatagramPacket instance is needed to receive messages that were sent to the client. 
			 */
			byte[] data =  new byte[256];
			DatagramPacket packet =  new DatagramPacket(data, data.length);
			
			/**
			 * The client application then enters an infinite loop where it blocks at the receive method
			 * until the server sends a message. Once the message has arrived, the message is displayed
			 */
			
			while(true)
			{
				multicastSocket.receive(packet);
				String message = new String(packet.getData(), 0, packet.getLength());
				System.out.println("Message from: "+ packet.getAddress() + " Message: ["+ message+ "]");
			}
		} catch (IOException ex) 
		{
			ex.printStackTrace();
			
		}
		System.out.println("UDP Multicast Time Client Terminated");
	}
	
	public static void main(String args[])
	{
		new UDPMulticastClient();
	}
}
