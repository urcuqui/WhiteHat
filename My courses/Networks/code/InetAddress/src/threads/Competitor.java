package threads;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class Competitor extends Thread {
	private JPanel box;
	private int x = 40;
	private int y = 40;
	private Color color;
	private int position;
	
	public Competitor(JPanel b, Color c, int p)
	{
		box = b;
		color = c;
		position = p;		
	}
	
	public void draw()
	{
		Graphics g = box.getGraphics();
		g.setColor(color);
		g.drawString("" + position + "-" + this.getPriority(), 10, position * 40);
		g.drawLine(x, position * y, x + 5, position * y);
		g.dispose();
	}
	
	public void move()
	{
		if(!box.isVisible())
		{
			return;
		}
		Graphics g = box.getGraphics();
		g.setXORMode(box.getBackground());
		g.setColor(color);
		while(x <= (box.getSize().width - 40))
		{
			g.drawLine(x, position * y, x + 5, position * y);
			x += 5;
			try
			{
				Thread.sleep(50);
			}catch(InterruptedException e)
			{
				System.out.println("Thread error");				
			}
		}
		g.drawString("T", box.getSize().width - 40 , position * y);
		g.dispose();
	}
	
	public void run()
	{
		draw();
		move();
	}
}
