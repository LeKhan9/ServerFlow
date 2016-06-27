import time
from socket import *
from random import *

'''________________________________________________________
Mohammad Khan
This is an implementation of a router that generates random
ip addresses in the subnet 130.0.0.0/18 at a rate of
approximately 3 packets/second and 130.0.128.0/18 at a rate
of 6 packets/second. Packets include a set message along with
an ip address and are sent via UDP.
______________________________________________________________'''

clientSocket = socket(AF_INET,SOCK_DGRAM)

while True:
    # every one second, 9 packets are generated
    for x in range(3):
        thirdDot1 = str(randrange(0,63))
        fourthDot = str(randrange(0,255))
        ipAddress1 = '130.0.' + thirdDot1 +'.' + fourthDot + '\nHELLO'
        ipAddress1 = ipAddress1.encode('ascii')
        clientSocket.sendto(ipAddress1,('localhost',10000))
    for y in range(6):
        thirdDot2 = str(randrange(128,191))
        fourthDot = str(randrange(0,255))
        ipAddress2 = '130.0.' + thirdDot2 +'.' + fourthDot + '\nHELLO'
        ipAddress2 = ipAddress2.encode('ascii')
        clientSocket.sendto(ipAddress2,('localhost',10000))

    time.sleep(1)

clientSocket.close()
