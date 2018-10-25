package udp_multicasting;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.net.StandardSocketOptions;
import java.nio.ByteBuffer;
import java.nio.channels.DatagramChannel;

public class UDPDatagramMulticastServer {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		/**
		 * Let's use the System class's setProperty method to specify that IPv6
		 * be used
		 */
		System.setProperty("java.net.preferIPv6Stack", "true");
		try {
			// Once connected, a datagram channel remains connected until it is disconnected or closed.
			// https://docs.oracle.com/javase/7/docs/api/java/nio/channels/DatagramChannel.html
			DatagramChannel channel = DatagramChannel.open();
			NetworkInterface networkInterface =  NetworkInterface.getByName("wlan0");
			// The setOption method will associate the channel with the network interface 
			// that was used to identify the group
			channel.setOption(StandardSocketOptions.IP_MULTICAST_IF, networkInterface);
			InetSocketAddress group = new InetSocketAddress("FF01:0:0:0:0:0:0:FC", 9003);
			
			// A byte buffer is then created, based on a message string.
			String message =  "The message";
			ByteBuffer buffer = ByteBuffer.allocate(message.length());
			buffer.put(message.getBytes());
			
			// Inside the while loop, the buffer is sent out to group members.
			while(true)
			{
				channel.send(buffer, group);
				System.out.println("Sent the multicast message: " +  message);
				buffer.clear();
				
				buffer.mark();
				System.out.println("Sent: [");
				StringBuilder msg =  new StringBuilder();
				while(buffer.hasRemaining()) //Tells whether there are any elements between the current position and the limit
				{
					msg.append((char) buffer.get());				
				}
				System.out.println(msg + "]");
				buffer.reset();
				Thread.sleep(1000);
			}
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

}
