package threads;

public class Bank {

	private int [] accounts;
	private int totalValue = 1000000;
	private int transactionNum = 0;
	
	
	public Bank()
	{
		accounts = new int[10]; // we will have 10 accounts
		for(int accountNum = 0; accountNum < 10; accountNum++)
		{
			accounts[accountNum] = 100000;
		}
	}
	
	public int getTransactionNum()
	{
		return transactionNum;
	}
	
	public int getAccountValue(int accountNum)
	{
		return accounts[accountNum];
	}
	
	public int getTotalValue()
	{
		return totalValue;
	}
	
	public void setTransactionNum()
	{
		transactionNum++ ;
	}
	
	/*public void setAccountValue(int accountNum, int value)
	{
		accounts[accountNum] += value;
		totalValue += value;
	}*/
	public synchronized void setAccountValue(int accountNum, int value)
	{
		accounts[accountNum] += value;
		totalValue += value;
	}
}
