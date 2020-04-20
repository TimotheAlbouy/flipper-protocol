from scapy.all import *

# golden ratio
FLPR_PORT = 16180


class FLPR(Packet):
    name = "FLPR"
    fields_desc = [
        ShortField("id", random.getrandbits(16)),
        FieldLenField("ctr", None, count_of="hist"),
        ByteField("lim", random.getrandbits(8)),
        FieldListField("hist", None, IPField("", "0.0.0.0"), count_from=lambda pkt: pkt.ctr)
    ]
