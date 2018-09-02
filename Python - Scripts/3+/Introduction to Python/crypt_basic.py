# Python 3
# It is only useful in UNIX systems
# Author: Christian Urcuqui
# Book reference: Stoll, C., & Connolly, J. W. (1990). The cuckoo's egg: Tracking a spy through the maze of computer
# espionage. Physics Today, 43, 75.
import crypt

help(crypt)
# we will try hashing a password using the crypt() function, to do this we will
# pass the password 'egg' and the salt "HX"
print(crypt.crypt('egg', 'HX'))

# this is the result of the previous function HX9LLTdc/jiDE


