import binascii	
import re
from Crypto.Cipher import AES
import sys
from zipfile import ZipFile

def unknownVer(conf):
        with open(sys.argv[1], 'rb') as jar:
            fileData = binascii.hexlify(jar.read())
            if '636f6e6669672e646174' in fileData:
                key = fileData.split('636f6e6669672e646174')[2][0:32]
                iv =  fileData.split('636f6e6669672e646174')[2][32:64]
                return unknownVerAESDecrypt(key,iv,conf)
            else:
                print "[+] Fail to decrypt"
   
def unknownVerAESDecrypt(key,iv,conf):
    unpad = lambda s : s[0:-ord(s[-1])]
    cipher = AES.new(key.decode("hex"), AES.MODE_CBC, iv.decode("hex") )
    confhex = binascii.hexlify(conf)
    return unpad(cipher.decrypt(confhex.decode("hex")))
    
try:
	conf = None
	with ZipFile(sys.argv[1], 'r') as zip:
		for name in zip.namelist():
			if name == "config.dat": 
				conf = zip.read(name)
	print unknownVer(conf)

except:
	print "File Not Found"
