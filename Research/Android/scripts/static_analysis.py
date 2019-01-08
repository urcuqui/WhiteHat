__author__ = 'Christian Urcuqui'
# This class generates all information for ML
import Permissions_Android
import xml.etree.ElementTree as ET
import os
import csv
import numpy as np


def eraser(package):
    os.system("find " + "Output/" + package + " -type f ! -name 'AndroidManifest.xml' -delete")


def manifestBinaryVector(package):
    # open a file csv
    fl = open('binaryApps.csv', 'w')
    # writer = csv.writer(fl, delimiter=' ',
    #                    quotechar='|', quoting=csv.QUOTE_NONE)

    lstDir = os.walk(package)
    binaryPermisionsbyApp = []
    salida = []
    a = 0
    array_output = ''
    #for root, dirs, files in lstDir:
    #    if root != package:
    try:
        print(package + "/AndroidManifest.xml")
        tree = ET.parse(package + "/AndroidManifest.xml")
        treeRoot = tree.getroot()
        array_permissions = []

        for permission in treeRoot.findall('uses-permission'):
            per = permission.get('{http://schemas.android.com/apk/res/android}name')
            array_permissions.append(per)

        binaryPermisionsbyApp.append(package.partition('/')[2])
        array_output = package.partition('/')[2] + ','
        for item in sorted(Permissions_Android.AOSP_PERMISSIONS):

            if array_permissions.__contains__(item):
                binaryPermisionsbyApp.append('1')
                array_output += '1,'
            else:
                binaryPermisionsbyApp.append('0')
                array_output += '0,'

        fl.write(array_output + '\n')
        array_output = ''
        print("wrote..")
    except:
        print("error")


class Manifest:

    def start(self, dname):
        fileList = os.listdir(dname)
        for filename in fileList:
            os.system("apktool" + " " + "d -f "+dname+"/"+filename+" -o" + "Output/"+filename)
            eraser(filename)
            manifestBinaryVector("Output/"+filename)




    # a = np.array(binaryPermisionsbyApp)
    # print (a)
    # print(np.shape(a))
    # np.savetxt('binary.csv',np, delimiter=',', fmt="%s")

    def eraser(package):
        os.system("find " + "Output/" + package + " -type f ! -name 'AndroidManifest.xml' -delete")
