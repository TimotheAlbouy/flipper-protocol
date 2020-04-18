import sys
from scapy.all import *

from impl.constants import FLPR_PORT


class FLPR(Packet):
    name = "FLPR"
    fields_desc = [
        ShortField("id", random.getrandbits(16)),
        ShortField("bnc", random.getrandbits(16)),
        FieldLenField("len", None, count_of="hist"),
        FieldListField("hist", [], IPField("", "0.0.0.0"), count_from=lambda pkt: pkt.len)
    ]


bind_layers(TCP, FLPR, sport=FLPR_PORT)
bind_layers(TCP, FLPR, dport=FLPR_PORT)
