import subprocess
import time
import os

#Inicializacion del abd
os.chdir("..")
os.chdir("Sdk/emulator")
subprocess.Popen(["./emulator -avd Pixel_XL_API_26 -port 5037"], shell=True) # En lugar de Pixel_XL_API_26 se debe colocar el nombre del emulador que se va a usar, los espacios son remplazados por guiones bajos y se debe elegir un puerto si se requiere, Android usa el 5037 por defecto.

os.system("gnome-terminal -x sh -c 'cd ..;cd ..;cd Traffic-generator;python instalacionApp.py; exec bash'")




