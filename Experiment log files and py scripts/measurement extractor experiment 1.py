# argv.py
import sys



i=0
rssi_values=[]
rssi_total=0

no_connection_count = 0

packets = []

with open(sys.argv[1]) as txtfile:
    for line in txtfile:
        if ("Signal strengh is" in line):
           i += 1
           rssi_values.append(int(line[37:40]))
           rssi_total += int(line[37:40])
        if ("Not reachable yet" in line):
            no_connection_count += 1
        
        if ("[WARN: App       ] Tx/Rx/MissedTx: " in line):
            packets.append(line[35:-1].split("/"))

print("Signal strengh amount of lines: " + str(i))
print("rssi value count: " + str(len(rssi_values)))

#print("mean of rssi values: " + str(rssi_total/len(rssi_values)))

print("count of not reachable: " + str(no_connection_count))


print("packets send/recieved/missed: " + str(int(packets[-1][0])-int(packets[0][0])) + "/" + str(int(packets[-1][1])-int(packets[0][1])) + "/" +str(no_connection_count))#str(int(packets[-1][2])-int(packets[0][2])) )