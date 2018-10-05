# Date: 1 Oct 2018
# Author: Christian Urcuqui
# [0][1][0]
# [0][0][1]
# [1][1][1]
# Reference: O'Connor, T. (2012). Violent Python: a cookbook for hackers, forensic analysts, penetration testers and security engineers.
# Make Zip files with secret passwords

import zipfile
import threading
import optparse

global notFind

def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password)
        print("[+] Password = " + str(password) + "\n")
        notFind = False
    except:
        notFind = True
        pass


def main():
    notFind = True
    parser = optparse.OptionParser("usage%prog -f <zipfile> -d <dictionary>")
    parser.add_option("-f", dest="zname", type="string", help="specify zip file")
    parser.add_option("-d", dest="dname", type="string", help="specify dictionary file")
    (options, args) =  parser.parse_args()
    if (options.zname == None) | (options.dname == None):
        print(parser.usage)
        exit(0)
    else:
        zname = options.zname
        dname =  options.dname
    zFile = zipfile.ZipFile(zname)
    passFile = open(dname)
    for line in passFile.readlines():
        if(notFind):
            password = line.strip('\n')
            t = threading.Thread(target=extractFile, args=(zFile, password.encode()))
            t.start()
        else:
            exit(0)


if __name__ == "__main__":
    main()
