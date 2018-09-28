package webserver_logs;
import java.io.*;
import java.util.*;
import java.util.concurrent.*;
/**
 * it contains the main() method that reads the file and creates one LookupTask per line
 * Moreover, it requires Java 7 for try-with-resources and multi-catch 
 * This class allows us to print the hostname associated to each IP in a log file
 * This is the first example of to analyze the logs from the book:
 * Hughes, M., Shoffner, M., Hamner, D., Winslow, M., & Hughes, C. (1997). 
 * Java network programming (Vol. 2). Greenwich/CT: Manning.
 * @author Christian Urcuqui
 * [0][1][0]
 * [0][0][1] 
 * [1][1][1]
 */
public class PooledWeblog 
{

	private final static int NUM_THREADS = 4;
	
	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		Scanner scanner = new Scanner(System.in);
		String dir = "";
		do
		{
			System.out.println("Write the path of the log file");
			dir = scanner.nextLine();	
		
			ExecutorService executor = Executors.newFixedThreadPool(NUM_THREADS);
			Queue<LogEntry> results = new LinkedList<LogEntry>();
			try (BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(dir), "UTF-8"));) 
			{
				for (String entry = in.readLine(); entry != null; entry = in.readLine()) 
				{
					LookupTask task = new LookupTask(entry);
					Future<String> future = executor.submit(task);
					LogEntry result = new LogEntry(entry, future);
					results.add(result);
				}
			} catch (UnsupportedEncodingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			// Start printing the results. This blocks each time a result isn't ready.
			for (LogEntry result : results) 
			{
				try 
				{
					System.out.println(result.future.get());
				} catch (InterruptedException | ExecutionException ex) 
				{
					System.out.println(result.original);
				}
			}
			executor.shutdown();
		}while(dir.equals("exit")==false);
	}
	private static class LogEntry 
	{
		String original;
		Future<String> future;
		LogEntry(String original, Future<String> future) 
		{
			this.original = original;
			this.future = future;
		}
	}
	
}



