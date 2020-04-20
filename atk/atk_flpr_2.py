from scapy.all import *

from impl.flpr import FLPR, FLPR_PORT
from impl.util import send_flpr, random_ip, own_ip


# create a new ball with his own IP in the history
def atk_flpr_2():
    src = own_ip()
    dst = random_ip()
    id = random.getrandbits(16)
    lim = random.getrandbits(8)
    hist = [src]
    send_flpr(dst, id, lim, hist)
    print("new illegal ball created, ID = %s" % id)


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    atk_flpr_2()
