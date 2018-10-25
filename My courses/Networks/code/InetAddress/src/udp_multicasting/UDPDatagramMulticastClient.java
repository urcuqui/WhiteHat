package udp_multicasting;

import java.io.IOException;
import java.net.*;
import java.nio.*;
import java.nio.channels.DatagramChannel;
import java.nio.channels.MembershipKey;

public class UDPDatagramMulticastClient {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.setProperty("java.net.preferIPv6Stack", "true");
		try {
			NetworkInterface networkInterface =  NetworkInterface.getByName("wlan0");
			
			DatagramChannel channel = DatagramChannel.open()
					.bind(new InetSocketAddress(9003))
					.setOption(StandardSocketOptions.IP_MULTICAST_IF,
					networkInterface);
			/**
			 * The group is then created based on the same IPv6 address that was used by the
			   server, and a MembershipKey instance is created using the channel's join method
			 */
			InetAddress group =
					InetAddress.getByName("FF01:0:0:0:0:0:0:FC");
					MembershipKey key = channel.join(group, networkInterface);
			System.out.println("Joined Multicast Group: "+ key);
			System.out.println("Waiting for a message...");
			
			ByteBuffer buffer =  ByteBuffer.allocate(1024);
			channel.receive(buffer);
			
			// To display the contents of the buffer, we need to flip it.
			buffer.flip();
			System.out.println("Received: [");
			StringBuilder message =  new StringBuilder();
			while(buffer.hasRemaining())
			{
				message.append((char) buffer.get());
			}
			System.out.println(message + "]");
			key.drop();
		} catch (SocketException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

}
