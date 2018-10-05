# Date: 1 Oct 2018
# Author: Christian Urcuqui
# [0][1][0]
# [0][0][1]
# [1][1][1]
# Reference: O'Connor, T. (2012). Violent Python: a cookbook for hackers, forensic analysts, penetration testers and security engineers.
# Make Zip files with secret passwords

import zipfile

zFile = zipfile.ZipFile("evil.zip")
try:
    zFile.extractall(pwd="secret".encode())
except Exception as e:
    print(e)
print("the files were extracted from the file zip ")
