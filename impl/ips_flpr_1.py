from scapy.all import *

from flpr import FLPR, FLPR_PORT
from ifaces import ifaces
from util import ban_ip


# verify that the same IP does not appear 2 times in a row in the history
def ips_flpr_1(pkt):
    ip = pkt[IP]
    flpr = pkt[FLPR]
    print("flipper message received, ID = %s, CTR = %s, LIM = %s" % (flpr.id, flpr.ctr, flpr.lim))
    i = 0
    while i < len(flpr.hist) - 1:
        if flpr.hist[i] == flpr.hist[i+1]:
            print("ATTACK DETECTED: new ball with several IP in history")
            print()
            ban_ip(ip.src)
            return
    print("message forwarded")
    print()


if __name__ == "__main__":
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print("listening for FLPR on TCP port %s" % FLPR_PORT)
    # intercept only incoming FLPR messages
    sniff(prn=ips_flpr_1, iface=ifaces, lfilter=lambda pkt: FLPR in pkt and pkt[Ether].src != Ether().src)
