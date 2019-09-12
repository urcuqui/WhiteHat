import subprocess

install=subprocess.call(["ls Apps > apps.txt"], shell=True) #cambiar Apps por el nombre de la carpeta donde se encuentran las aplicaciones


listaApps = open("apps.txt", "r") #Es un log de las aplicaciones procesadas
listaAppsCompleta=open("datasetMal.txt", "w") #Archivo generado al final con las rutas de las aplicaciones
t=0;
for s in listaApps.readlines():
	s2=s.strip()
        ruta="/home/webdev/Android/ArchivosTrafico/Apps/"  #Cambiar por la ruta absoluta de la carpeta donde se encuentran las aplicaciones 
	listaAppsCompleta.write(ruta+s2+'\n')
	t=t+1

print t
listaAppsCompleta.close()
listaApps.close()

