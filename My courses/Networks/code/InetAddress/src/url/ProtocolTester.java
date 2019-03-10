package url;

import java.net.*;

/**
 * This is a protocol tester example from the book:
 * Hughes, M., Shoffner, M., Hamner, D., Winslow, M., & Hughes, C. (1997). 
 * Java network programming (Vol. 2). Greenwich/CT: Manning.
 * @author 	Christian Urcuqui
 * [0][1][0]
 * [0][0][1] 
 * [1][1][1]
 */
public class ProtocolTester {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		// hypertext transfer protocol
		testProtocol("http://www.adc.org");
		// secure http
		testProtocol("https://www.amazon.com/exec/obidos/order2/");
		// file transfer protocol
		testProtocol("ftp://ibiblio.org/pub/languages/java/javafaq/");
		// Simple Mail Transfer Protocol
		testProtocol("mailto:elharo@ibiblio.org");
		// telnet
		testProtocol("telnet://dibner.poly.edu/");
		// local file access
		testProtocol("file:///etc/passwd");
		// gopher
		testProtocol("gopher://gopher.anc.org.za/");
		// Lightweight Directory Access Protocol
		testProtocol(
		"ldap://ldap.itd.umich.edu/o=University%20of%20Michigan,c=US?postalAddress");
		// JAR
		testProtocol(
		"jar:http://cafeaulait.org/books/javaio/ioexamples/javaio.jar!"
		+ "/com/macfaq/io/StreamCopier.class");
		// NFS, Network File System
		testProtocol("nfs://utopia.poly.edu/usr/tmp/");
		// a custom protocol for JDBC
		testProtocol("jdbc:mysql://luna.ibiblio.org:3306/NEWS");
		// rmi, a custom protocol for remote method invocation
		testProtocol("rmi://ibiblio.org/RenderEngine");
		// custom protocols for HotJava
		testProtocol("doc:/UsersGuide/release.html");
		testProtocol("netdoc:/UsersGuide/release.html");
		testProtocol("systemresource://www.adc.org/+/index.html");
		testProtocol("verbatim:http://www.adc.org/");
		
	}
	
	private static void testProtocol(String url)
	{
		try
		{
			URL u = new URL(url);
			System.out.println(u.getProtocol() + " is supported");		
		}catch (MalformedURLException ex) {
			String protocol = url.substring(0, url.indexOf(':'));
			System.out.println(protocol + " is not supported");
		}
	}
}
