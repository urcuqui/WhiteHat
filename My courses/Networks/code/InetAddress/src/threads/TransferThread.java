package threads;

import tools.core;

public class TransferThread extends Thread
{
	private Bank theBank;
	private int source;
	
	public TransferThread(ThreadGroup group, Bank theBank, int source)
	{
		super(group, ""+source);
		this.theBank = theBank;
		this.source = source;
	}
	
	public void run()
	{
		while(true)
		{
			int destination;
			do 
			{
				destination = core.randomWithRange(0, 9);	
			}while(destination == source);
			
			int quantity = core.randomWithRange(0, 10000);
			theBank.setAccountValue(source, quantity * -1);
			theBank.setAccountValue(destination, quantity);
			theBank.setTransactionNum();
			int transaction = theBank.getTransactionNum();
			if(transaction%10000==0)
			{
				System.out.println("Transaction="+transaction+" Total="+theBank.getTotalValue());				
			}			
		}
	}
}
