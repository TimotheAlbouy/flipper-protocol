from scapy.all import *

from impl.flpr import FLPR, FLPR_PORT, send_flpr, random_ip
from impl.pool import pool


def verify_flpr(pkt):
    if FLPR in pkt:
        print("FLPR message received.")
        flpr = pkt.payload.payload.payload
        if flpr.lim != 0:
            if flpr.ctr == flpr.lim:
                winner_ip = max(set(flpr.hist), key=flpr.hist.count)
                print("The winner of the ball %s is %s." % (flpr.id, winner_ip))
            elif flpr.ctr == flpr.lim - 1:
                flpr.hist.append("0.0.0.0")
                for ip in pool:
                    send_flpr(ip, flpr.id, flpr.lim, flpr.hist)
            elif flpr.ctr < flpr.lim - 1:
                dest = random_ip()
                flpr.hist.append(dest)
                send_flpr(dest, flpr.id, flpr.lim, flpr.hist)


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print("Listening for FLPR message...")
    flt = "tcp and port %s" % FLPR_PORT
    sniff(filter=flt, prn=verify_flpr)
