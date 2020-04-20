from scapy.all import *

from .flpr import FLPR, FLPR_PORT
from .util import send_flpr, random_ip


def start_ball():
    dst = random_ip()
    id = random.getrandbits(16)
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        lim = int(sys.argv[1])
    else:
        lim = random.getrandbits(8)
    hist = [dst]
    send_flpr(dst, id, lim, hist)
    print("new ball created, ID = %s" % id)
    print("time: %s" % time.time())


if __name__ == "__main__":
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    start_ball()
