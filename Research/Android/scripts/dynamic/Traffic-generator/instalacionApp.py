# -*- coding: utf-8 -*-
import subprocess
import time
import os
import sys

#preparacion del directorio del emulador
time.sleep(20)
print os.getcwd()
#instalacion de una app
archivo=open("datasetPrueba.txt", "r")
os.chdir("..")
os.chdir("Sdk/platform-tools")

listaPa = open("paquetesFallidos.txt", "w")
listaApps = open("instalacionesFallidas.txt", "w")
cantidad=0
paqueteAUsar=""

for g in archivo.readlines():
	try:
		commandR="./adb install " + g 
		commandSE=commandR.strip()
		instalador=commandSE+" > estadoInstalacion.txt"
		print instalador
		install=subprocess.call([instalador], shell=True)
		variableEstado=open("estadoInstalacion.txt", "r")
		fileLineas=variableEstado.readlines()
		variableEstado.close()
		ultimaLinea=fileLineas[len(fileLineas)-1]
		ultimaLineaSE=ultimaLinea.strip()
 		
		if ultimaLineaSE=="Success":	
			print "instalada"			
			time.sleep(30)
			detenerAVD="./adb kill-server"
			subprocess.call([detenerAVD], shell=True)
			reconectarHost="./adb reconnect"
			subprocess.call([reconectarHost], shell=True)
			reconectarAVD="./adb reconnect device"
			subprocess.call([reconectarAVD], shell=True)
			time.sleep(5)
			subprocess.call(["./adb reboot"], shell= True)
			time.sleep(10)
			#obtencion de paquetes
			subprocess.Popen(['./adb root'], shell=True)
			prueba='./adb shell "pm list packages -3"'

			packages=subprocess.Popen([prueba],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = packages.communicate()
			f = open('paquetes.txt','w')
			f.write(out)
			f.close()

			archivoPack=open('paquetes.txt','r')
			nombreArchivoPartido=g.split('.')
			nombreArchivoPartido2=nombreArchivoPartido[0].split("APPS/") #Cambiar Apps por el nombre de la carpeta donde se encuentran las aplicaciones
			nombreArchivo=nombreArchivoPartido2[1]
			print "el nombre del archivo es: "+ nombreArchivo
			
			for s in archivoPack.readlines():
				#if nombreArchivo in s:
				paqueteCompleto=s.split(':')
				nombrePaquete=paqueteCompleto[1]
				nombrePaquete2=nombrePaquete.strip()
				if nombrePaquete2!="com.example.android.apis":
					

					paqueteAUsar=nombrePaquete2
					wiresharkInicio="tshark -i 17 -a duration:300 -w /home/jsvillatech/Android/Capturas/"+paqueteAUsar+".pcap" #cambiar em1 por su interfaz de red
#ejecucion monkey 
					#comandoMonkey="./adb -e shell monkey --ignore-crashes -p "+nombrePaquete2+" -v --throttle 6000 300"
					print "Iniciando monkey"
#se debe cambiar el proximo comando dependiendo del OS donde se está ejecutando el sistema de captura
#Actualmente funciona con Ubuntu
					os.system("gnome-terminal -- sh -c 'cd /home/jsvillatech/Android/Traffic-generator/; python2 monkeyR.py'")

					subprocess.call([wiresharkInicio],shell=True)
					
					#subprocess.call([comandoMonkey],shell=True)
#completar desinstalacion
					des="./adb shell pm uninstall -k "+nombrePaquete2
					subprocess.call([des],shell=True)
					print "Se ha desinstalado el paquete:"+ nombrePaquete2
					time.sleep(30)			
					subprocess.call(["./adb reboot"], shell =True)
					time.sleep(10)
					print "finish"
		
				else:
					
					listaPa.write(g)
					

			archivoPack.close()
		else:
			cantidad=cantidad+1;
			listaApps.write(g+", "+ultimaLineaSE+"\n")
			
			print "error con la aplicacion"	
	except IOError as e:
		t = open("errores.txt", "w")
		t.write("I/O error({0}): {1}".format(e.errno, e.strerror)+"\n")
		t.close()
listaApps.close()
listaPa.close()
archivo.close()
print "cantidad de fallidas: "+ str(cantidad)







