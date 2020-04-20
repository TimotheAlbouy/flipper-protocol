from scapy.all import *

response_ports = []


def verify_pkt(pkt):
    global response_ports
    if UDP in pkt:
        print("UDP is not allowed.")
    elif TCP in pkt:
        # transport layer segment (TCP or UDP)
        tcp = pkt.payload.payload
        if tcp.dport == 80:
            print("Forwarding request on port %s." % tcp.dport)
            response_ports.append(tcp.sport)
            send(pkt)
        elif tcp.dport in response_ports:
            print("Forwarding response on port %s." % tcp.dport)
            response_ports.remove(tcp.dport)
            send(pkt)
        else:
            print("Port %s is not allowed." % tcp.dport)


if __name__ == "__main__":
    conf.color_theme = ColorOnBlackTheme()
    print("Listening for all TCP or UDP segments.")
    f = "tcp or udp"
    sniff(filter=f, prn=verify_pkt)