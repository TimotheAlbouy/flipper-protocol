from scapy.all import *

from constants import FLPR_PORT


class FLPR(Packet):
    name = "FLPR"
    fields_desc = [
        ShortField("id", random.getrandbits(16)),
        ShortField("bnc", random.getrandbits(16)),
        FieldLenField("len", None, count_of="hist"),
        FieldListField("hist", [], IPField("", "0.0.0.0"), count_from=lambda pkt: pkt.len)
    ]


def verify_flpr(pkt):
    pkt.show()


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    flt = "tcp and port %s" % FLPR_PORT
    sniff(filter=flt, prn=verify_flpr)
