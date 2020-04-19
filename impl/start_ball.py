from scapy.all import *

from impl.flpr import FLPR, FLPR_PORT, send_flpr, random_ip


def start_ball():
    dest = random_ip()
    id = random.getrandbits(16)
    lim = random.getrandbits(8)
    hist = [dest]
    ball = send_flpr(dest, id, lim, hist)
    send(ball)
    print("New FLPR ball created, ID = %s." % id)


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    start_ball()
