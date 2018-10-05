package udp;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Date;

public class NewsUDPServerControl extends NewsUDPServer{
	public final static int DEFAULT_PORT = 9000;
	protected BufferedReader fileReader =  null;
	protected boolean moreNews = true;
	
	
	public NewsUDPServerControl() 
	{
		super(DEFAULT_PORT);
		try 
		{
			fileReader = new BufferedReader(new FileReader("D:/Usuarios/rhaps/Documents/GitHub/WhiteHat/My courses/Networks/code/InetAddress/src/udp/news.txt"));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			System.err.println("It is not possible to open the news file");
		}
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		NewsUDPServerControl server = new NewsUDPServerControl();
		Thread t = new Thread(server);
		t.start();
		
	}

	/**
	 * The next method allows us to write the logic behind the server answer 
	 */
	@Override
	public void respond(DatagramSocket socket, DatagramPacket request) throws IOException {
		// TODO Auto-generated method stub
		/* We are going to get the address and the port from the client */
		InetAddress address = request.getAddress();
		int port = request.getPort();
		System.out.println("Request received from:" + address.getHostAddress());
		while(moreNews)
		{
			//We are going to get the data about the answer
			String news = null;
			if(fileReader == null)
			{
				news = new Date().toString();
			}
			else 
			{
				news = getNew();
				byte[] buf = news.getBytes();
				
				/*We are going to send the answer to the client */
				DatagramPacket threadSendPacket =  new DatagramPacket(buf, buf.length, address, port);
				try {
					socket.send(threadSendPacket);
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
					moreNews =  false;
				}
			}			
		}
		
		
	}
	protected String getNew()
	{
		String news = null;
		try {
			if((news = fileReader.readLine()) == null)
			{
				fileReader.close();
				moreNews = false;
				news = "No more news";
			}
			else
			{
				
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			news = "The server has an IOException";
		}
		return news;
	}
	
	

}
