from scapy.all import *

from impl.constants import FLPR_PORT

if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    flt = "tcp and port %s" % FLPR_PORT
