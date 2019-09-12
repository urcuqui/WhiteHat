import os
import subprocess

contador=0
os.chdir("../Sdk/platform-tools")
subprocess.Popen(['./adb root'], shell=True)
prueba='./adb shell "pm list packages -3"'

packages=subprocess.Popen([prueba],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = packages.communicate()
f = open('paquetesTerceros.txt','w')
f.write(out)
f.close()

archivoPack=open('paquetesTerceros.txt','r')
for s in archivoPack.readlines():
  paqueteCompleto=s.split(':')
  nombrePaquete=paqueteCompleto[1]
  nombrePaquete2=nombrePaquete.strip()
  if nombrePaquete2!="com.example.android.apis":
    des="./adb shell pm uninstall -k "+nombrePaquete2
    subprocess.call([des],shell=True)
    contador=contador+1

print "Se han desinstalado "+str(contador) +" paquetes"


