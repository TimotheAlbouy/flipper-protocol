import sys
from scapy.all import IP, sr1, ICMP

a = IP(ttl=10)
print(a.src)
