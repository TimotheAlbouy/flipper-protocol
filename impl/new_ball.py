import sys
from scapy.all import *

from impl.flpr import FLPR
from impl.constants import FLPR_PORT

if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    ball = IP(dst="192.168.1.15")/TCP(sport=FLPR_PORT, dport=FLPR_PORT)/FLPR()
    res = sr1(ball)
    print(res)
