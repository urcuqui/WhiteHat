/**
 * Multicasting is the process of sending to multiple clients (group) at the same time. Each client must join a multicast group.
 * Multicast is the old IPV4 CLASS D and uses address 244.0.0.0 through 239.255.255.255.
 * Author: Christian Urcuqui
 */
package udp_multicasting;

import java.io.IOException;
import java.net.*;
import java.util.*;

public class UDPMulticastServer {

	public UDPMulticastServer()
	{
		System.out.println("UDP Multicast Time Server Started");
		try {
			MulticastSocket multicastSocket = new MulticastSocket();
			InetAddress inetAddress = InetAddress.getByName("228.5.6.7");
			multicastSocket.joinGroup(inetAddress);
			
			byte[] data;
			DatagramPacket packet;
			
			/** The server application will use an infinite loop to broadcast a new date and time 
			*	every  second. The thread is paused for one second, and then a new date and time
			*   is created using the Data class.  
			**/
			while(true)
			{
				Thread.sleep(1000);
				String message =  (new Date()).toString();
				System.out.println("Sending: [" + message + "]");
				data =  message.getBytes();
				packet =  new DatagramPacket(data, message.length(), inetAddress, 9877);
				multicastSocket.send(packet);
				
			}
			
		} catch (IOException | InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
			System.out.println(
			"UDP Multicast Time Server Terminated");
	}
	public static void main(String args[]) 
	{
		new UDPMulticastServer();		
	}
	
	
}
