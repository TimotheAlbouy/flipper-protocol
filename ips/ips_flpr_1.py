from scapy.all import *

from impl.flpr import FLPR, FLPR_PORT

ball_histories = {}


# verify that the new history is adding just 1 IP address from the previous IP
def verify_flpr(pkt):
    global ball_histories
    if FLPR in pkt:
        print("flipper message received")
        flpr = pkt.payload.payload.payload
        if flpr.id not in ball_histories:
            print("new ball")
            ball_histories[flpr.id] = flpr.hist
            print("new ball history saved")
            send(pkt)
            print("message forwarded")
        else:
            print("existing ball")
            if ball_histories[flpr.id] != flpr.hist[:-1]:
                print("ATTACK DETECTED: invalid new history for ball ID")
            else:
                send(pkt)
                print("message forwarded")


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print("listening for FLPR on TCP port %s" % FLPR_PORT)
    f = "tcp and port %s" % FLPR_PORT
    sniff(filter=f, prn=verify_flpr)