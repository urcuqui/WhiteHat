package threads;

public class BankAdministrative {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		// it makes the bank and it's accounts
		Bank theBank = new Bank();
		System.out.println(theBank.getTotalValue());
		
		// it makes the group of threads
		ThreadGroup threadsGroup = new ThreadGroup("Bank Threads");
		
		// it makes the threads and saves them in an array
		Thread[] threadsArray = new Thread[10];
		for(int index=0; index<threadsArray.length; index++)
		{
			threadsArray[index] = new TransferThread(threadsGroup, theBank, index);			
		}
		for(int index=0; index<threadsArray.length; index++)
		{
			threadsArray[index].start();
		}
		
	}

}
