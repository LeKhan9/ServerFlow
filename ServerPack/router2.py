from socket import *

'''________________________________________________________
Mohammad Khan
This is an implementation of a router that takes in random
packets coming in from another router, parses them to retrieve
ip addresses which then get crosslisted with a forwarding table.
This demonstrates a mock router whereby two different ISPs are
able to receive packets from a single router.
______________________________________________________________'''

serverPort = 10000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("RECEIVING PACKETS TO FORWARD")

# reads the destinations into a list
fileName = open('router2_ftable.txt')
destinations = [dest.rstrip('\n') for dest in fileName]

# ordering the destinations in the forwarding table file by
# longest prefix, the idea is to hit a longer prefix first,
# and break out versus prematurely being forwarded to a shorter one
forward = []
while destinations:
    # sorting by number of *s in the ranges
    minlength = min(s.count('*') for s in destinations)
    for t in destinations:
        if t.count('*') == minlength:
            indexer = destinations.index(t)
            forward.append(destinations.pop(indexer))

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode('ascii')

    # splitting, getting ip address from payload
    ipAddress = modifiedMessage.split('\n')
    print(ipAddress[0])
    y = ipAddress[0].split('.');

    # converts third dot to binary, for testing purposes
    binary = bin(int(y[2])).split('0b')
    padZeros = ''
    for x in range(8-len(binary[1])):
        padZeros += '0'
    third = padZeros + binary[1]

    # converting fourth dot to binary, for testing purposes
    binary = bin(int(y[3])).split('0b')
    padZeros = ''
    for x in range(8-len(binary[1])):
        padZeros += '0'
    fourth = padZeros + binary[1]

    
    # retrieving the four different blocks from the ipAddresses
    first = int(y[0])
    second = int(y[1])
    third = int(y[2])
    fourth = int(y[3])

    modifiedMessage = modifiedMessage.encode('ascii')

    # looking through the forwarding table for a match
    for y in forward:
        y = y.split(' ')

        # conversion of the binary into int in order to compare
        # lower range and upper range by padding with zeros and ones
        # respectively - this also figures for dropped packages
        firstBlock = int(y[0],2)
        secondBlock = int(y[1],2)
        del y[:2]
        del y[3:]
        min1 = int(y[0].replace('*','0'),2)
        max1 = int(y[0].replace('*','1'),2)
        min2 = int(y[1].replace('*','0'),2)
        max2 = int(y[1].replace('*','1'),2)

        # since /18, compares first and second block for equality and then compares
        # ranges for each block range in 3rd,4th blocks --> then send to appropriate isp
        if( (firstBlock == first) and (secondBlock == second) and
            (min1 <= third <= max1) and (min2 <= fourth <= max2)):
            if(y[2] == '0'):
                serverSocket.sendto(modifiedMessage, ('localhost',11000))

            if(y[2] == '1'):
                serverSocket.sendto(modifiedMessage, ('localhost',12000))


clientSocket.close()
            
    

