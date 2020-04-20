from scapy.all import *

from flpr import FLPR, FLPR_PORT
from ifaces import ifaces
from util import ban_ip

ball_histories = {}


# verify that the new history is adding just 1 IP address from the old history
def ips_flpr_1(pkt):
    global ball_histories
    ip = pkt[IP]
    flpr = pkt[FLPR]
    print("flipper message received, ID = %s, CTR = %s, LIM = %s" % (flpr.id, flpr.ctr, flpr.lim))
    if flpr.id not in ball_histories:
        print("new ball")
        if len(flpr.hist) > 1:
            print("ATTACK DETECTED: new ball with several IP in history")
            ban_ip(ip.src)
        else:
            ball_histories[flpr.id] = flpr.hist
            print("new ball history saved")
            print("message forwarded")
    else:
        print("existing ball")
        if ball_histories[flpr.id] != flpr.hist[:-1]:
            print("ATTACK DETECTED: new history not based on previous one")
            ban_ip(ip.src)
        else:
            print("message forwarded")
    print()


if __name__ == "__main__":
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print("listening for FLPR on TCP port %s" % FLPR_PORT)
    # intercept only incoming FLPR messages
    sniff(prn=ips_flpr_1, iface=ifaces, lfilter=lambda pkt: FLPR in pkt and pkt[Ether].src != Ether().src)
