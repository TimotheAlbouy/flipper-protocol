from scapy.all import *

from impl.flpr import FLPR, FLPR_PORT

ball_histories = {}


# verify that the new history is adding just 1 IP address from the old history
def ips_flpr_1(pkt):
    global ball_histories
    flpr = pkt[FLPR]
    print("flipper message received, ID = %s, CTR = %s, LIM = %s" % (flpr.id, flpr.ctr, flpr.lim))
    if flpr.id not in ball_histories:
        if len(flpr.hist) > 1:
            print("ATTACK DETECTED: new ball with several IP in history")
        else:
            ball_histories[flpr.id] = flpr.hist
            print("new ball history saved")
            send(pkt, verbose=False)
            print("message forwarded")
    else:
        if ball_histories[flpr.id] != flpr.hist[:-1]:
            print("ATTACK DETECTED: new history not based on previous one")
        else:
            send(pkt, verbose=False)
            print("message forwarded")
    print()


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print("listening for FLPR on TCP port %s" % FLPR_PORT)
    # intercept only incoming FLPR messages
    sniff(prn=ips_flpr_1, lfilter=lambda pkt: pkt[Ether].src != Ether().src and FLPR in pkt)
