#!/usr/bin/env python3
"""
shutarp - identifies top arp requesters from the output of 'monitor traffic interface' in Junos.

"""

__author__ = "Ben Dale - ben.dale@gmail.com"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from collections import Counter

def process_capture_file(fd):
    arp_sources=[]
    for packet in fd:
        header = packet.split()
        if header[1:4] == ['In', 'arp', 'who-has']:  # without Junos 'layer2-headers' knob
            arp_sources.append(header[len(header)-1]) # record the last field of header (the ARP source IP)
        elif (header[1] == 'In') & (header[16:18] == ['arp', 'who-has']): # with Junos 'layer2-headers' knob
            arp_sources.append(header[len(header)-1])
    return (arp_sources)


def main(args):
    try:
        fd = open(args.capture_file, 'r')
    except IOError:
        print ("I/O Error - there was an error opening the file")
        return
    except FileNotFoundError:
        print ("File not found - check filename and path")
        return
    except:
        raise
        return
    arp_sources = process_capture_file(fd)
    fd.close()
    source_count = Counter()
    for arp_source in arp_sources:
        source_count[arp_source] += 1
    print ("Top " + args.topn + " ARP request sources:\n")
    for source in source_count.most_common(int(args.topn)):
        print("{0:15s} : {1:6d}".format(source[0], source[1]))
    print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", help="capture file name", action="store", dest="capture_file", required=True)

    parser.add_argument("-t", "--topn", help="show top n ARPers", dest="topn", default='10')

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)