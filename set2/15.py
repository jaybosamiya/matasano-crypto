from common import unpad

try:
    unpad("ICE ICE BABY\x04\x04\x04\x04")
    print "[+] Unpadded correctly"
except:
    print "[-] Should not have thrown exception."

try:
    unpad("ICE ICE BABY\x05\x05\x05\x05")
    print "[-] Should have thrown exception"
except:
    print "[+] Threw exception properly"

try:
    unpad("ICE ICE BABY\x01\x02\x03\x04")
    print "[-] Should have thrown exception"
except:
    print "[+] Threw exception properly"

