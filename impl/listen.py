import sys
from collections import Counter

from scapy.all import *

from impl.flpr import FLPR, FLPR_PORT
from impl.util import send_flpr, random_ip, own_ip
from impl.pool import pool


def elect_winner(hist):
    scores = Counter(hist).most_common()
    high_score = scores[0][1]
    winners = []
    for s in scores:
        if s[1] < high_score:
            break
        winners.append(s[0])
    print("winner(s) of ball: %s" % winners)


def handle_flpr(pkt):
    flpr = pkt[FLPR]
    print("received FLPR[id=%s, ctr=%s, lim=%s, hist=%s]" % (flpr.id, flpr.ctr, flpr.lim, flpr.hist))
    if flpr.lim == 0:
        print("do nothing")
    elif flpr.ctr == flpr.lim:
        elect_winner(flpr.hist)
    elif flpr.ctr == flpr.lim - 1:
        flpr.hist.append("0.0.0.0")
        for ip in pool:
            if ip == own_ip():
                pass
            send_flpr(ip, flpr.id, flpr.lim, flpr.hist)
        print("scores communicated")
        elect_winner(flpr.hist)
    elif flpr.ctr < flpr.lim - 1:
        dst = random_ip()
        flpr.hist.append(dst)
        print(dst)
        send_flpr(dst, flpr.id, flpr.lim, flpr.hist)
        print("ball resent")
    else:
        print("do nothing")


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print("listening for FLPR on TCP port %s" % FLPR_PORT)
    # intercept only incoming FLPR layers
    sniff(prn=handle_flpr, lfilter=lambda pkt: pkt[Ether].src != Ether().src and FLPR in pkt)
