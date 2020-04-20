from scapy.all import *

from .flpr import FLPR, FLPR_PORT


# verify that the last IP in history is the sender's IP
def ips_flpr_2(pkt):
    ip = pkt[IP]
    flpr = pkt[FLPR]
    print("flipper message received, ID = %s, CTR = %s, LIM = %s" % (flpr.id, flpr.ctr, flpr.lim))
    if not flpr.hist:
        print("ATTACK DETECTED: history is empty")
    elif flpr.ctr == flpr.lim:
        print("scores communication")
        send(pkt, verbose=False)
        print("message forwarded")
    elif ip.src != flpr.hist[-1]:
        print("ATTACK DETECTED: last IP in history and sender's IP not matching")
    else:
        print("regular message")
        send(pkt, verbose=False)
        print("message forwarded")
    print()


if __name__ == "__main__":
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print("listening for FLPR on TCP port %s" % FLPR_PORT)
    # intercept only incoming FLPR messages
    sniff(prn=ips_flpr_2, lfilter=lambda pkt: pkt[Ether].src != Ether().src and FLPR in pkt)
