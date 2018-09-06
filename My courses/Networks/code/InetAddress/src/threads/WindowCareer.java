package threads;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class WindowCareer extends javax.swing.JFrame {

	private JPanel canvas;
	private Competitor threads[] = new Competitor[3];
	private Color colors[] = {Color.blue, Color.red, Color.green};
	private JLabel etPriority1, etPriority2, etPriority3 = null;
	private JTextField priority1, priority2, priority3 = null;
	
	public WindowCareer() {
		setSize(600, 300);
		setTitle("Career");
		
		/** the next lines are important to add in this example **/
		Container contentPane = getContentPane();
		contentPane.setLayout(new BorderLayout());
		
		canvas = new JPanel();
		contentPane.add(canvas, "Center");
		
		JPanel p = new JPanel();
		p.setLayout(new FlowLayout());
		addCompetitors(p);
		contentPane.add(p, "North");
		
		JPanel p1 = new JPanel();
		addButton(p1, "Start Match", new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				threads[0] = new Competitor(canvas, colors[0], 1);
				threads[0].setPriority(Integer.parseInt(priority1.getText()));
				
				threads[1] = new Competitor(canvas, colors[1], 2);
				threads[1].setPriority(Integer.parseInt(priority2.getText()));
				
				threads[2] =  new Competitor(canvas, colors[2], 3);
				threads[2].setPriority(Integer.parseInt(priority3.getText()));
				
				for(int countThreads = 0; countThreads < 3; countThreads++) {
					threads[countThreads].start();
					//threads[countThreads].run();					
				}
				for(int countThreads = 0; countThreads < 3; countThreads++) {
					//threads[countThreads].start();
					threads[countThreads].run();					
				}
			}
		});		
		
		addButton(p1, "Finish", new ActionListener() {			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				canvas.setVisible(false);
				System.exit(0);
			}
		});
		contentPane.add(p1, "South");
		
	}
	
	public void addButton(Container c, String title, ActionListener a)
	{
		JButton b = new JButton(title);
		c.add(b);
		b.addActionListener(a);
		
	}
	public void addCompetitors(Container c)
	{
		etPriority1 = new JLabel("Competitor's priority 1:");
		priority1 = new JTextField(2);
		c.add(etPriority1);
		c.add(priority1);
		
		etPriority2 = new JLabel("Competitor's priority 2:");
		priority2 = new JTextField(2);
		c.add(etPriority2);
		c.add(priority2);
		
		etPriority3 =  new JLabel("Competitor's priority 3:");
		priority3 = new JTextField(2);
		c.add(etPriority3);
		c.add(priority3);
	}
	
}


