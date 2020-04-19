from scapy.all import *

from impl.pool import pool

# golden ratio
FLPR_PORT = 16180


class FLPR(Packet):
    name = "FLPR"
    fields_desc = [
        ShortField("id", random.getrandbits(16)),
        FieldLenField("ctr", None, 8, count_of="hist"),
        ByteField("lim", random.getrandbits(8)),
        FieldListField("hist", None, IPField("", "0.0.0.0"), count_from=lambda pkt: pkt.ctr)
    ]


def send_flpr(dest, id, lim, hist):
    send(IP(dest=dest)/TCP(sport=FLPR_PORT, dport=FLPR_PORT)/FLPR(id=id, lim=lim, hist=hist))


def random_ip():
    own_ip = IP().src
    drawn_ip = random.choice(pool)
    while drawn_ip == own_ip:
        drawn_ip = random.choice(pool)
    return drawn_ip
