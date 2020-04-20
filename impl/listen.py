from collections import Counter
from uuid import getnode as own_mac

from scapy.all import *

from impl.flpr import FLPR, FLPR_PORT
from impl.util import send_flpr, random_ip
from impl.pool import pool


def handle_flpr(pkt):
    if FLPR in pkt:
        flpr = pkt[FLPR]
        print("received FLPR[id=%s, ctr=%s, lim=%s, hist=%s]" % (flpr.id, flpr.ctr, flpr.lim, flpr.hist))
        if flpr.lim == 0:
            print("do nothing")
        elif flpr.ctr == flpr.lim:
            winners = Counter(flpr.hist).most_common()
            print("winner(s) of ball %s:" % flpr.id)
            for w in winners:
                ip, nb = w
                print(ip)
        elif flpr.ctr == flpr.lim - 1:
            flpr.hist.append("0.0.0.0")
            for ip in pool:
                send_flpr(ip, flpr.id, flpr.lim, flpr.hist)
            print("scores communicated")
        elif flpr.ctr < flpr.lim - 1:
            dst = random_ip()
            flpr.hist.append(dst)
            print(dst)
            send_flpr(dst, flpr.id, flpr.lim, flpr.hist)
            print("ball resent")
        else:
            print("do nothing")


def filter_flpr(pkt):
    return pkt[Ether].src != own_mac() and FLPR not in pkt


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print("listening for FLPR on TCP port %s" % FLPR_PORT)
    #f = "tcp port %s" % FLPR_PORT
    # lambda pkt: pkt[Ether].src != own_mac() and FLPR not in pkt
    sniff(prn=handle_flpr, lfilter=filter_flpr)
