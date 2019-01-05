import os
#import Permissions_Android
#from Generator import Manifest
from os import listdir
from os.path import isfile
import optparse



""" Author:  Christian Urcuqui
    Last update: 24 November 2018
    Description: This project makes a dataset with features from static analysis and 
    dynamic analysis. It is neccesary to use this tool with root privileges    
"""



apktool_dir = "/usr/local/bin/apktool.bat"
"""apktool_dir = "sudo apktool"""
dir_apk = "cd .."
package_output = "output"


def menu():
    # This is the command menu
    log = " ___   ___    __   ____  ___    ___    __    __               ".join("\n")
      .join("|   | /  |   |  |  |  |  |  |  /  |   |  |  |  |      [0][1][0]   ").join("\n")
#    +   "|   |/  /    |  |  |  |  |  | /  /    |  |  |  |         [0][0][1]    " + "\n"
#"|      /     |  |  |  |  |      |      \  \_/  /         [1][1][1]    \n" +
#"|  |\  \     |  '--'  |  |  |\  \        \   /                        \n" +
#"| _| `.__\   |________|  | _| `.__\      |___|                        \n"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$_$$$$$$$$$$$$$$$$_$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$__$$$$$$$$$$$$$$_$$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$$_______________$$$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$$$___________________$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$____$$$_________$$$____$$$$$$$$$$$$$
# $$$$$$$$$$$$$_____$$$_________$$$_____$$$$$$$$$$$$
# $$$$$$$$$$$$___________________________$$$$$$$$$$$
# $$$$$$$$$$$$___________________________$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# $$$$_____$$$____________________________$$$____$$$
# $$$$_____$$$____________________________$$______$$
# $$$$_____$$$____________________________$$______$$
# $$$$_____$$$____________________________$$______$$
# $$$$_____$$$____________________________$$______$$
# $$$$_____$$$____________________________$$______$$
# $$$$_____$$$____________________________$$______$$
# $$$$______$$____________________________$$______$$
# $$$$_____$$$____________________________$$______$$
# $$$$$___$$$$____________________________$$$___$$$$
# $$$$$$$$$$$$____________________________$$$$$$$$$$
# $$$$$$$$$$$$____________________________$$$$$$$$$$
# $$$$$$$$$$$$___________________________$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$______$$$$$$_____$$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$______$$$$$$_____$$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$______$$$$$$_____$$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$______$$$$$$_____$$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$______$$$$$$_____$$$$$$$$$$$$$$$$
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$




    print(log)


    parser = optparse.OptionParser("Make dataset -d <dictionary> -a <analysis>")
    parser.add_option("-d", dest="dname", type="string", help="APK dictionary")
    parser.add_option("-a", dest="aname", type="string", help="type of analysis")
    (options, args) = parser.parse_args()
    if(options.dname is None) | (options.dname is None):
        print(parser.usage)
        exit(0)
    else:
        aname = options.aname
        dname = options.dname



class AndroidRE:

    #Use the ApkTool over a list of Apks
    def ApkTooldefragmenter(self):

        fileList = os.listdir("Samples")

        for filename in fileList:
            os.system(apktool_dir + " " + "d -f "+"/root/Desktop/Cookie/Samples/"+filename+" -o" + "Output/"+filename)
            self.eraser(filename)
    #Erase all files except a androidmanifest.xml
    def eraser(self, package):
      os.system("find " +"Output/"+package+ " -type f ! -name 'AndroidManifest.xml' -delete")

#c = AndroidRE()
#c.ApkTooldefragmenter()


if __name__ == "__main__":
    menu()

