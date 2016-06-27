from socket import *

'''________________________________________________________
Mohammad Khan
This is an implementation of a ISP router that takes incoming
packets (simulated simply with ip addresses) and distributes
them among a set number of subnets which is defined through
a forwarding table file. 
__________________________________________________________'''

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("RECEIVING PACKETS FROM ROUTER2")

# reads the destinations into a list
fileName = open('ispb_ftable.txt')
subs = [x.rstrip('\n') for x in fileName]

# to keep track of number of packets that have come
# in to be within the range of each Subnet; counters
subCount = [0] * len(subs)

        
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode('ascii')

    # gets the incoming ip address and parses it for comparison
    # with table from text file 
    ipAddress = modifiedMessage.split('\n')
    
    # y has the ip address coming in, we get each block
    y = ipAddress[0].split('.');
    first = int(y[0])
    second = int(y[1])
    third = int(y[2])
    fourth = int(y[3])

    for t in subs:
        t = t.split(' ')
        output = t[2]
        ipSlash = t[0].split('/')

        # obtains ip and slash number, to get the # of stars
        ip = ipSlash[0]
        slash = int(ipSlash[1])
        numStars = 32 - (slash)

        # z holds each block of the ip
        z = ip.split('.')

        # converts whole ip into a binary string
        fullBinary = ''
        for u in z:
            binary = bin(int(u)).split('0b')
            padZeros = ''
            for v in range(8-len(binary[1])):
                padZeros += '0'
            u = padZeros + binary[1]
            fullBinary += u

        #adds *s to the portion of ip that is dynamic
        clean = fullBinary[0:slash]
        for ty in range(numStars):
            clean += '*'

        # splitting back into original blocks
        block1 = clean[0:8]
        block2 = clean[8:16]
        block3 = clean[16:24]
        block4 = clean[24:32]

        # these switches will determine if incoming ip fits in range
        block1Switch = False
        block2Switch = False
        block3Switch = False
        block4Switch = False

        # all these cases below check for ip in range, or
        # if the block is not dynamic then checks for equality 
        if('*' in block1):
            min1 = int(block1.replace('*','0'),2)
            max1 = int(block1.replace('*','1'),2)
            if(min1 <= first <= max1):
                block1Switch = True
        else:
            if(first == int(block1,2)):
                block1Switch = True

        if('*' in block2):
            min1 = int(block2.replace('*','0'),2)
            max1 = int(block2.replace('*','1'),2)
            if(min1 <= second <= max1):
                block2Switch = True
        else:
            if(second == int(block2,2)):
                block2Switch = True

        if('*' in block3):
            min1 = int(block3.replace('*','0'),2)
            max1 = int(block3.replace('*','1'),2)
            if(min1 <= third <= max1):
                block3Switch = True
        else:
            if(third == int(block3,2)):
                block3Switch = True

        if('*' in block4):
            min1 = int(block4.replace('*','0'),2)
            max1 = int(block4.replace('*','1'),2)
            if(min1 <= fourth <= max1):
                block4Switch = True
        else:
            if(fourth == int(block4,2)):
                block4Switch = True
        
        # if we have a hit, increment at that bin
        if((block1Switch == True) and (block2Switch == True) and
           (block3Switch == True) and (block4Switch == True)):
            subCount[int(output)] +=1
    
        # prints the hit count of each subnet
        print('----------------')
        for x in range(len(subCount)):
            y = str(subCount[x])
            print('SUB'+ str(x) + ' ' + y + ' packets')
        print('----------------')

