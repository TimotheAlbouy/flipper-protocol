from scapy.all import *

from impl.flpr import FLPR, FLPR_PORT, send_flpr, random_ip
from impl.pool import pool


def handle_flpr(pkt):
    if FLPR in pkt:
        flpr = pkt.payload.payload.payload
        print("received FLPR[id=%s, ctr=%s, lim=%s, hist=%s]" % (flpr.id, flpr.ctr, flpr.lim, flpr.hist))
        if flpr.lim == 0:
            print("do nothing")
        elif flpr.ctr == flpr.lim:
            winner_ip = max(set(flpr.hist), key=flpr.hist.count)
            print("winner of ball is %s" % winner_ip)
        elif flpr.ctr == flpr.lim - 1:
            flpr.hist.append("0.0.0.0")
            for ip in pool:
                send_flpr(ip, flpr.id, flpr.lim, flpr.hist)
            print("scores communicated")
        elif flpr.ctr < flpr.lim - 1:
            dest = random_ip()
            flpr.hist.append(dest)
            send_flpr(dest, flpr.id, flpr.lim, flpr.hist)
            print("ball resent")
        else:
            print("do nothing")


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print("listening for FLPR on TCP port %s" % FLPR_PORT)
    f = "tcp port %s" % FLPR_PORT
    sniff(filter=f, prn=handle_flpr)
