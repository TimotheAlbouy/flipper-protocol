import sys
from scapy.all import *

from impl.constants import FLPR_PORT


def verify_flpr(pkt):
    pkt.show()


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    flt = "tcp and port %s" % FLPR_PORT
    sniff(filter=flt, prn=verify_flpr)
