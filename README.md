# ServerFlow
Several programs in python to simulate the forwarding operation of a router and the distribution function of an ISP. 

Router 1 is a standalone python program called router1.py. 
It generates packets with random destination IP addresses in the subnet 130.0.0.0/18 at a rate of approximately 3 packets/second
and 130.0.128.0/18 at a rate of 6 packets/second. Packets consist of strings only with IP numbers in dotted notation on the first 
line and a second line with some fixed text that acts as the payload. This information will be sent using UDP packets.

Router 2 is another standalone python program called router2.py. It is a process listening on port 10000 to which router 1 will send 
its packets. This router does not have a queue. It reads its forwarding table from a file called router2_ftable.txt. The file contains 
information about the IP ranges for each outgoing link. If the IP of the incoming packet does not match the ranges in the table the 
packet is dropped. The table is given in binary notation using the symbols 0, 1, and *, for example:

10000010 00000000 00****** ******** 0
10000010 00000000 010***** ******** 0 
10000010 00000000 10****** ******** 1 
10000010 00000000 11****** ******** 1
The rightmost number indicates the outgoing link (0 for the left output and 1 for the right output).

ROUTER 1
ROUTER 2
ISP A
ISP B

ISP A is yet another standalone python program called ispa.py. It is a process listening on port
11000. It can receive UDP packets and forwards them to its customer subnets as defined in the
file ispa_ftable.txt. The IP ranges are given in slash notation where each entry is on a separate
line, for example:
130.0.0.0/24 SUB0
130.0.1.0/24 SUB 1
130.0.2.0/24 SUB 2
130.0.3.0/24 SUB 3
….
130.0.7.0/24 SUB 7
Similar to the router data file above these numbers are not fixed and can change based on the
configuration so your program should read and interpret them accordingly. Here, the subnets
are indexed and there should be as many lines in the file as there are subnets. Assume there is
one set of equally divided subnets and if the IP of the incoming packet does not match the
ranges in the table the packet is dropped.
With the arrival of each packet, ISP A displays the packet arrivals to all its subnets as follows:
SUB0 28 packets
SUB1 47 packets
SUB2 73 packets
…
SUB7 108 packets

ISP B is a similar process listening on port 12000 with its source program in the file called
ispb.py.

Run all four programs simultaneously and observe their operation through the text output of the
ISP A and ISP B console windows.
