package Buffers;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Example_Buffer {
	
	
	/**
	 * Metodo que realiza la suma de dos numeros
	 */
	private static int sumaNumeros(int numero1 , int numero2) {
		
		return numero1 + numero2 ;
	}
	
	
	public static void main(String[] args) {
			
		 BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		 BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		 
		 
		 try {
			String[] cadena = br.readLine().split(";");
			int suma = sumaNumeros(Integer.parseInt(cadena[0]), Integer.parseInt(cadena[1]));
			bw.write(suma + "");
			bw.flush();
			br.close();
			bw.close();
			
		}
		 
		 catch (IOException e) {
			System.out.println("Se presento un error en la lectura de consola");
		}
	}
	

}
