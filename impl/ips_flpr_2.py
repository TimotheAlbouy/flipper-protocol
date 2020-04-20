from subprocess import call

from scapy.all import *

from flpr import FLPR, FLPR_PORT
from ifaces import ifaces


# verify that the last IP in history is the sender's IP
def ips_flpr_2(pkt):
    ip = pkt[IP]
    flpr = pkt[FLPR]
    print(f"flipper message received, ID = {flpr.id}, CTR = {flpr.ctr}, LIM = {flpr.lim}")
    if not flpr.hist:
        print("ATTACK DETECTED: history is empty")
        call(f"iptables -A INPUT -s {ip.src} -p tcp --destination-port {FLPR_PORT} -j DROP")
    elif flpr.ctr == flpr.lim:
        print("scores communication")
        print("message forwarded")
    elif ip.src != flpr.hist[-1]:
        print("ATTACK DETECTED: last IP in history and sender's IP not matching")
        call(f"iptables -A INPUT -s {ip.src} -p tcp --destination-port {FLPR_PORT} -j DROP")
    else:
        print("regular message")
        print("message forwarded")
    print()


if __name__ == "__main__":
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print(f"listening for FLPR on TCP port {FLPR_PORT}")
    # intercept only incoming FLPR messages
    sniff(prn=ips_flpr_2, iface=ifaces, lfilter=lambda pkt: FLPR in pkt and pkt[Ether].src != Ether().src)
