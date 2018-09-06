package threads;
import java.io.*;

/** This is the class of the example ShowMainMessage with ThreadGroup **/
public class ShowMainMessage2 {

	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		
		// Make a ThreadGroup
		ThreadGroup threadsGroup = new ThreadGroup("Thread Group");
		
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		System.out.println("Write the number of threads to execute");
		try {
			
			// The next code makes the ThreadGroup
			int threadsNumbers = Integer.parseInt(br.readLine()) ;
			ShowMessage[] arrayThread = new ShowMessage[threadsNumbers];
			for(int index=0; index <arrayThread.length; index++)
			{
				//arrayThread[index] = new ShowMessage("Thread" + (index+1));
				arrayThread[index] = new ShowMessage(threadsGroup, "Thread" + (index+1));
			}
			for(int index=0; index<arrayThread.length; index++)
			{
				arrayThread[index].start();
			}
			// Note that the method join() helps us to synchronize each thread, for this case
			// in an ascendant way, so what will happen if we don't use it?				
//			for(int index=0; index<arrayThread.length; index++)
//			{
//				try {
//					arrayThread[index].join();
//				} catch (InterruptedException e) {
//					// TODO Auto-generated catch block
//					e.printStackTrace();
//				}
//			}
			// our threads will be part of a loop until some thread will not be active
			while(threadsGroup.activeCount() == arrayThread.length) {};
			
			// now we will stop all the threads in the group
			threadsGroup.interrupt();
			
			
			// The next lines will get the longest time
			int longest = -1, longestPosition = -1;
			for(int index=0; index<arrayThread.length; index++)
			{
				if(arrayThread[index].getWaitTime()> longest)
				{
					longest = arrayThread[index].getWaitTime();
					longestPosition =  index;
				}
			}
			System.out.println("The most delayed thread was " + arrayThread[longestPosition].getName() + 
					" with a time of " + longest + " milseconds");
		} catch (NumberFormatException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
