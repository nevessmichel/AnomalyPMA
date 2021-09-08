# import PMA model
from model import PMA
# import lib to process tcpdump
from scapy.utils import RawPcapReader

# function to process frame status


def frameFeedback(status, frame, predicted):
    print("___________________________")
    print("status: {} \nframe: {} \npredicted: {}".format(status, frame, predicted))

# function to handle tcpdump


def pcap(file_name):
    print('Opening {}...'.format(file_name))
    # size of window
    size = 100
    #interval in secs
    interval = 10
    # initialize model
    pma = PMA(frameFeedback, size)
    # package counter
    count = 0
    # iterate in all packages
    for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
        # increment counter
        count += 1
        # verify if is first iteration
        if count == 1:
            # set model start time
            pma.setStart(pkt_metadata.sec, interval)
        # send package time to model
        pma.packageIn(pkt_metadata.sec)
    # end model
    pma.stop()

    print('{} contains {} packets'.format(file_name, count))


if ("__main__" == __name__):
    # files to test
    files = ["Data/week1/monday.tcpdump"]
    # iterate files
    for f in files:
        # call tcpdump handler
        pcap(f)
