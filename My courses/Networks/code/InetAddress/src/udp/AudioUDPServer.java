/**
 * Author: Christian Urcuqui
 * Date: 25 october 2018
	• AudioFormat: This class specifies the characteristics of the audio format that
	is used. As there are several audio formats available, the system needs to
	know which one is being used.
	• AudioInputStream: This class represents the audio that is being recorded
	or played.
	• AudioSystem: This class provides access to the system's audio devices
	and resources.
	• DataLine: This interface controls operations applied against a stream, such
	as starting and stopping a stream.
	• SourceDataLine: This represents the destination of the sound, such
	as a speaker.
	• TargetDataLine: This represents the source of the sound, such as
	a microphone.
	Refence: Harold, E. (2004). Java network programming. " O'Reilly Media, Inc.".
 */
package udp;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.TargetDataLine;

public class AudioUDPServer {

	private final byte audioBuffer [] = new byte[10000];
	private TargetDataLine targetDataLine;
	
	/**
	 * The constructor uses a setupAudio method to initialize the audio
	 * and a broadcastAudio method to send this audio to a client
	 */
	public AudioUDPServer()
	{
		setupAudio();
		broadcastAudio();
	}
	
	/**
	 * the next method specifies the audio-stream characteristics
	 * Big endian and little endian refers to the order of bytes.
	 * Big endian means that the most-significant byte of a word is stored at the smallest memory address
	 * least significant byte at the largest memory address.
	 * Little endian reverses this order.
	 * @return the audio format
	 */
	private AudioFormat getAudioFormat()
	{
		float sampleRate = 16000F;
		int sampleSizeInBits =  16;
		int channels = 1;
		boolean signed = true;
		boolean bigEndian = false;
		return new AudioFormat(sampleRate, sampleSizeInBits, channels, signed, bigEndian);
	}
	
	/**
	 * The DataLine.Info class uses the audio format information to create a line representing audio.
	 * The AudioSystem class's getLine method returns a data line that corresponds to a microphone.
	 */
	private void setupAudio()
	{
		try
		{
			AudioFormat audioFormat = getAudioFormat();
			DataLine.Info dataLineInfo =  new DataLine.Info(TargetDataLine.class, audioFormat);
			targetDataLine = (TargetDataLine) AudioSystem.getLine(dataLineInfo);
			targetDataLine.open(audioFormat);
			targetDataLine.start();
		} catch(Exception ex)
		{
			ex.printStackTrace();
			System.exit(0);
		}
	}
	
	private void broadcastAudio()
	{
		try
		{
			DatagramSocket socket = new DatagramSocket(8000);
			InetAddress inetAddress = InetAddress.getByName("127.0.0.1");
			
			/**
			 * An inifite loop is entered where the read method fills the audioBuffer array and 
			 * returns the number of bytes read. For counts grater than 0, a new packet is made using
			 * the buffer and is sent to the client listening on port 9786
			 */
			while(true)
			{
				int count = targetDataLine.read(audioBuffer, 0, audioBuffer.length);
				if(count>0)
				{
					DatagramPacket packet =  new DatagramPacket(audioBuffer, audioBuffer.length, inetAddress, 9786);
					socket.send(packet);
				}
			}
		} catch(Exception ex)
		{
			
		}
		
		
	}
	
	public static void main(String[] args) 
	{
		new AudioUDPServer();
	}

}
