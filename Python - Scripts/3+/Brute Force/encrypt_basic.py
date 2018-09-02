# Date: 1 Sept 2018
# Author: Christian Urcuqui
# Brute Force example through a password dictionary and a salt with users file to discover passwords

import crypt


# The next function receives the encrypted password as a parameter and returns either after
# finding the password or exhausting the words in the dictionary

def testPass(cryptPass):
    # Pay attention that the function first strips out the salt from the first two characters of the
    # encrypted password hash
    salt = cryptPass[0:2]
    dictFile = open('dictionary.txt', 'r')
    for word in dictFile.readlines():
        word = word.strip('\n')
        cryptWord = crypt.crypt(word, salt)
        if cryptWord == cryptPass:
            print("[+] Found Password: "+word+"\n")
            return
    print("[-] Password Not Found.\n")
    return


def main():
    passFile = open('passwords.txt')
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip(' ')
            print("[*] Cracking Password For: "+user)
            testPass(cryptPass)


if __name__=="__main__":
    main()