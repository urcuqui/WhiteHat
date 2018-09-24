package threads;

public class ShowMessage extends Thread {

	private int waitTime;
	
	public ShowMessage(String name)	
	{
		super(name);
		waitTime = (int) (Math.random() * 1000);		
	}
	// The next constructor is for the example with ThreadGroup
	public ShowMessage(ThreadGroup group, String name)
	{
		super(group, name);
		waitTime =  (int) (Math.random() * 100);
	}
	
	public int getWaitTime()
	{
		return waitTime;
	}
	
	public void run()
	{		
		try 
		{
			System.out.println("Start message - " + getName());
			Thread.sleep(waitTime);
			System.out.println("Final message - " + getName() + ":" + getWaitTime());
			
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			System.out.println("The "+getName() +" is sleeping");
			//e.printStackTrace();
		}		
	}	
}
