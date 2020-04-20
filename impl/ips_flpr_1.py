from subprocess import call

from scapy.all import *

from flpr import FLPR, FLPR_PORT
from ifaces import ifaces

ball_histories = {}


# verify that the new history is adding just 1 IP address from the old history
def ips_flpr_1(pkt):
    global ball_histories
    ip = pkt[IP]
    flpr = pkt[FLPR]
    print(f"flipper message received, ID = {flpr.id}, CTR = {flpr.ctr}, LIM = {flpr.lim}")
    if flpr.id not in ball_histories:
        print("new ball")
        if len(flpr.hist) > 1:
            print("ATTACK DETECTED: new ball with several IP in history")
            call(f"iptables -A INPUT -s {ip.src} -p tcp --destination-port {FLPR_PORT} -j DROP")
        else:
            ball_histories[flpr.id] = flpr.hist
            print("new ball history saved")
            print("message forwarded")
    else:
        print("existing ball")
        if ball_histories[flpr.id] != flpr.hist[:-1]:
            print("ATTACK DETECTED: new history not based on previous one")
            call(f"iptables -A INPUT -s {ip.src} -p tcp --destination-port {FLPR_PORT} -j DROP")
        else:
            print("message forwarded")
    print()


if __name__ == "__main__":
    bind_layers(TCP, FLPR, sport=FLPR_PORT)
    bind_layers(TCP, FLPR, dport=FLPR_PORT)
    print(f"listening for FLPR on TCP port {FLPR_PORT}")
    # intercept only incoming FLPR messages
    sniff(prn=ips_flpr_1, iface=ifaces, lfilter=lambda pkt: FLPR in pkt and pkt[Ether].src != Ether().src)
