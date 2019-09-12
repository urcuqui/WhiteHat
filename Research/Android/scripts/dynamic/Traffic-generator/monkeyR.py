# -*- coding: utf-8 -*-
import subprocess
import os

os.chdir("../Sdk/platform-tools")
archivoPack=open('paquetes.txt','r')

for s in archivoPack.readlines():
	paqueteCompleto=s.split(':')
	nombrePaquete=paqueteCompleto[1]
	nombrePaquete2=nombrePaquete.strip()

	if nombrePaquete2!="com.example.android.apis":	
		comandoMonkey="./adb -e shell monkey -p "+nombrePaquete2+" -v --throttle 5000 200"
		print "Este es el paquete: "+ nombrePaquete
		subprocess.call([comandoMonkey],shell=True)
		print "Done"

