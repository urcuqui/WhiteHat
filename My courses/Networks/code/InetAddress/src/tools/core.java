package tools;

public class core {
	
	public static int randomWithRange(int min, int max)
	{
	   int range = (max - min) + 1;     
	   return (int)(Math.random() * range) + min;
	}
	
	public static String getIP_decimal(byte add[])
	{
		int value;
		String result = "";
		for(int i=0; i<add.length; i++)
		{
			value = 0xff & add[i];
			// https://www.mkyong.com/java/java-and-0xff-example/
			// 0xff & is used to get the last 8 bits 
			result += value+ ".";				
		}
		return result;
	}
}
