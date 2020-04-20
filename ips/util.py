from scapy.all import *

from flpr import FLPR, FLPR_PORT
from pool import pool


def send_flpr(dst, id, lim, hist):
    flpr = IP(dst=dst)/TCP(sport=FLPR_PORT, dport=FLPR_PORT)/FLPR(id=id, lim=lim, hist=hist)
    send(flpr, verbose=False)


def own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


def random_ip():
    drawn_ip = random.choice(pool)
    while drawn_ip == own_ip():
        drawn_ip = random.choice(pool)
    return drawn_ip