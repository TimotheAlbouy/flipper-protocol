from collections import Counter

from scapy.all import *

from flpr import FLPR, FLPR_PORT
from util import send_flpr, random_ip, own_ip
from pool import pool


def elect_winner(hist, id):
    scores = Counter(hist).most_common()
    high_score = scores[0][1]
    winners = []
    for s in scores:
        if s[1] < high_score:
            break
        winners.append(s[0])
    print(f"winner(s) of ball {id}: {', '.join(winners)}")
    print(f"time: {time.time()}")


def handle_flpr(pkt):
    flpr = pkt[FLPR]
    print(f"flipper message received, ID = {flpr.id}, CTR = {flpr.ctr}, LIM = {flpr.lim}")
    if flpr.lim == 0:
        print("do nothing")
    elif flpr.ctr == flpr.lim:
        elect_winner(flpr.hist, flpr.id)
    elif flpr.ctr == flpr.lim - 1:
        flpr.hist.append("0.0.0.0")
        for ip in pool:
            if ip == own_ip():
                pass
            send_flpr(ip, flpr.id, flpr.lim, flpr.hist)
        print("scores communicated")
        elect_winner(flpr.hist, flpr.id)
    elif flpr.ctr < flpr.lim - 1:
        dst = random_ip()
        flpr.hist.append(dst)
        send_flpr(dst, flpr.id, flpr.lim, flpr.hist)
        print("ball sent back")
    else:
        print("do nothing")
    print()


if __name__ == "__main__":
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print(f"listening for FLPR on TCP port {FLPR_PORT}")
    # intercept only incoming FLPR messages
    sniff(prn=handle_flpr, lfilter=lambda pkt: FLPR in pkt and pkt[Ether].src != Ether().src)
