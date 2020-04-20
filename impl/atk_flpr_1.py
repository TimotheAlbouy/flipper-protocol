from scapy.all import *

from flpr import FLPR, FLPR_PORT
from util import send_flpr, random_ip, own_ip


# create a new ball with already 10 occurrences of his own IP in the history
def atk_flpr_1():
    src = own_ip()
    dst = random_ip()
    id = random.getrandbits(16)
    lim = random.getrandbits(8)
    hist = [src, src, src, src, src, src, src, src, src, src]
    send_flpr(dst, id, lim, hist)
    print("new illegal ball created, ID = %s" % id)


if __name__ == "__main__":
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    atk_flpr_1()
