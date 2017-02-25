from scapy.all import *

def querysniff(pkt):
            if Raw in pkt:
                payload = str(pkt[Raw].load)
                if "DKDN" in payload:
                    #print payload[9] + "",
                    sys.stdout.write(payload[9])

sniff(iface = "en0",filter = "tcp and port 24800", prn = querysniff, store = 0)
