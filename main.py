#system functions
import os, sys
#seconds to datetime lib
from datetime import datetime
# import lib to process tcpdump
from scapy.utils import RawPcapReader
# import scapy parser for ethernet protocol
from scapy.layers.l2 import Ether
# import scapy parser for IPV4 protocol
from scapy.layers.inet import IP
#import plot lib
import matplotlib.pyplot as plt
#matplotlib custom patches for legend
import matplotlib.patches as mpatches

# import PMA model
from model import PMA
#import arquive class
from arquive import Arquive

# function to process frame status

def frameFeedback(status, frame, predicted, time, interval):
    file = sys.argv[1]
    #class to handle file connection
    arq = Arquive(file)
    #append data to file
    arq.append(f'{status},{frame},{predicted},{time},{interval}\n')
    #print("___________________________")
    #print("status: {} \nframe: {} \npredicted: {}".format(status, frame, predicted))


# function to handle tcpdump

def pcap(file_name):
    print('Opening {}...'.format(file_name))
    # size of window
    size = 10
    #interval in secs
    interval = 5
    # initialize model
    pma = PMA(frameFeedback, size)
    # package counter
    count = 0
    # iterate in all packages as a vector of classes
    for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
        #print("__________________________")
        ether_pkt = Ether(pkt_data)
        #check if it's LLC protocol
        if 'type' not in ether_pkt.fields:
            #skip package
            continue
        # ignore non-IPv4 packets
        if ether_pkt.type != 0x0800:
            #skip package
            continue
        #parse IPV4 package
        ip_pkt = ether_pkt[IP]
        # Ignore non-TCP packet
        if ip_pkt.proto != 6:
            # skip package
            continue
        # increment counter
        count += 1
        #print(ip_pkt.dst)
        # verify if is first iteration
        if count == 1:
            # set model start time
            pma.setStart(pkt_metadata.sec, interval)
        # send package time to model
        pma.packageIn(pkt_metadata.sec)
    # end model
    pma.stop()
    #print('{} contains {} packets'.format(file_name, count))

def showResults():
    #open PMA result file
    arq = Arquive(sys.argv[1])
    #read file lines
    lines = arq.readAllLines()
    #status vector
    status_v = []
    #colors vector
    colors_v = []
    #frame vector
    frame_v = []
    #predict vector
    predict_v = []
    #count vector
    axis_x = []
    #count
    count = 1
    #remoce last line (empty)
    lines.pop()
    #color dict to parse status to colors
    color_dict = {"higher": "red", "lower": "yellow", "normal": "green", "training": "black"}
    highers = []
    lowers = []
    #iterate all lines
    for line in lines:
        #get data from line
        [status, frame, predict, time, interval] = line.split(",")
        #append color to vector
        colors_v.append(color_dict[status])
        #append status to vector
        status_v.append(status)
        #append frame parsed to int to vector
        frame_v.append(int(frame))
        #append predict parsed to float to vector
        predict_v.append(float(predict))
        #append count to vector
        axis_x.append(count)
        #cast time to int
        time = int(time)
        #cast interval to int
        interval = int(interval)
        #increment count
        count += 1
        if(status == "higher"):
            highers.append((datetime.fromtimestamp(time).strftime("%d/%m/%Y %I:%M:%S"), datetime.fromtimestamp(time+interval).strftime("%Y-%m-%d %I:%M:%S")))
        if(status == "lower"):
            lowers.append((datetime.fromtimestamp(time).strftime("%d/%m/%Y %I:%M:%S"), datetime.fromtimestamp(time+interval).strftime("%Y-%m-%d %I:%M:%S")))
    
    #print alerts Lower
    print(f"Alert Lower ({len(lowers)}):\n{lowers}")
    #print alerts Higher
    print(f"Alert Higher ({len(highers)}):\n{highers}")

    #create two subplots, one for lines, another to scatter
    fig, (ax1, ax2) = plt.subplots(2,1)
    #set subplot title
    ax1.set_title("Frames: Real vs Prediction")
    #plot frame data
    ax1.plot(axis_x, frame_v, label='Real', color="black")
    #plot predictions
    ax1.plot(axis_x, predict_v, label='Predicted', color = "blue")
    #create legend at lower right
    ax1.legend(loc="lower right")

    #set subplot title
    ax2.set_title("Frames: Status")
    #plot frame data as scatter plot
    ax2.scatter(axis_x, frame_v, c=colors_v, s=5)
    #create matplot custom legend data by color vs status
    handles = [mpatches.Patch(color=v, label=k) for k,v in color_dict.items()]
    #create legend at lower right
    ax2.legend(handles=handles, loc="lower right")
    #set spacing between subplots
    fig.tight_layout()
    #show plot
    plt.show()
    


if ("__main__" == __name__):
    #check if no file is passed as arg
    if(len(sys.argv) == 1):
        #append default file as sys args
        sys.argv.append("PMA_result.txt")
    #check if file already exists
    if os.path.exists(sys.argv[1]):
        #delete file
        #os.remove(sys.argv[1])
        pass
    # files to test
    files = ["Data/week4/monday.tcpdump"]
    # iterate files
    for f in files:
        # call tcpdump handler
        #pcap(f)
        break
    #show graphs
    showResults()
