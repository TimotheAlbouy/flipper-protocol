import socket

from scapy.all import *

from impl.pool import pool

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


def send_flpr(dst, id, lim, hist):
    send(IP(dst=dst)/TCP(sport=FLPR_PORT, dport=FLPR_PORT)/FLPR(id=id, lim=lim, hist=hist))


def own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


def random_ip():
    drawn_ip = random.choice(pool)
    while drawn_ip == own_ip():
        drawn_ip = random.choice(pool)
    return drawn_ip
