from scapy.all import *


def querysniff(pkt):
            if Raw in pkt:
                payload = str(pkt[Raw].load)
                if "DKDN" in payload:
                    sys.stdout.write(payload[9])
sniff(filter="tcp and port 24800", prn=querysniff, store=0)

