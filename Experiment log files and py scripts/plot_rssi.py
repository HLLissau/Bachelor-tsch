# argv.py
import sys
import re
import matplotlib.pyplot as plt 



rssi_values_parent=[]
rssi_values_server=[]

rssi_total=0

packet_diff = []
packet_missing=[]
missing_counter= 0

first = True
offsetx= 0
offsety= 0
offsetz= 0



with open(sys.argv[1]) as txtfile:
    for line in txtfile:
        if ("[WARN: RPL       ] relay inactive?:" in line):
           _,x,y = ([(-1)*int(i) for i in re.findall(r'\b\d+\b', line)])
           #print(x)
           #print(y)

           rssi_values_parent.append(x)
           rssi_values_server.append(y)
        if (("[WARN: App       ] Tx/Rx/MissedTx: " in line) and first == True):
            #print(line)
            #print((line[35:-1].split("/")))
            first = False

            offsetx,offsety,offsetz = (line[35:-1].split("/"))
            offsetx = int(offsetx)
            offsety = int(offsety)
            offsetz = int(offsetz)
            
            #packet_diff.append(int(x2)-int(y2))

        if ("[WARN: App       ] Tx/Rx/MissedTx: " in line):
            #print(line)
            #print((line[35:-1].split("/")))

            x2,y2,_ = (line[35:-1].split("/"))
            
            #packet_diff.append((int(x2)-offsetx)-(int(y2)-offsety))
            #packet_missing.append(int(z2)-offsetz)
            packet_diff.append((int(x2)-offsetx)-(int(y2)-offsety))
            packet_missing.append(missing_counter)
        
        if ("[INFO: App       ] Not reachable yet" in line):
            packet_diff.append(packet_diff[-1])
            rssi_values_parent.append(rssi_values_parent[-1])
            rssi_values_server.append(rssi_values_server[-1])

            missing_counter += 1
            packet_missing.append(missing_counter)

            


fig, ax = plt.subplots()

ax2 = ax.twinx()
ax2.bar(range(1,1+len(rssi_values_parent)), packet_diff,label="Tx - Rx" , color = "blue", alpha=.2)
ax2.bar(range(1,1+len(rssi_values_parent)), packet_missing,label="MissedTx" , color = "red", alpha=.2)
#ax2.set_ylim(0, max(max(packet_diff),max(packet_missing)) * 2)
ax2.set_ylim(0, max(20,max(packet_missing)*2))
if (missing_counter == 0):
    ax2.set_yticks(range(0,20+1))


ax.plot(range(1,1+len(rssi_values_parent)),rssi_values_parent,label="Parent RSSI", color= "green")
ax.plot(range(1,1+len(rssi_values_parent)),rssi_values_server,label="Server RSSI",color= "red")

ax.set_zorder(ax2.get_zorder()+1)
ax.set_frame_on(False)

ax.set_xlabel("packet number")
ax.set_ylabel("RSSI")
#plt.plot(range(1,1+len(rssi_values_parent)),rssi_values_parent,rssi_values_server)
#plt.legend(['Parent', 'Server'])
handles, labels = ax.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
combined_handles = handles + handles2
combined_labels = labels + labels2
ax.legend(combined_handles, combined_labels, loc='upper center')

print(packet_diff)
plt.show()

#print("rssi value count: " + str(len(rssi_values)))

#print("mean of rssi values: " + str(rssi_total/len(rssi_values)))
