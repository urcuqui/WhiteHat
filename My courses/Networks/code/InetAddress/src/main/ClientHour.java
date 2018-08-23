package main;
import java.net.*;
import java.io.*;
import java.util.*;
public class ClientHour {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		String row;
		String address =  "0.0.0.0";
		int port = 13;
		InetAddress server = null;
		try {
			server = InetAddress.getByName(address);
			System.out.println(server);
			Socket socket = new Socket(server, port);			
			System.out.println( "The socket is open!" );
			
			OutputStream out = socket.getOutputStream();
			
			Writer ok = new OutputStreamWriter(socket.getOutputStream());
		    ok.write("What is the hour? \\r\\n");
		    out.flush();
		    InputStream in = new BufferedInputStream(socket.getInputStream());
		    int c;
			    while ((c = in.read()) != -1)
			    {
			      System.out.write(c);
			    }
			// the next close process is necessary
			    socket.close();
			in.close();
			in.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

}
