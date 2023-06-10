# argv.py
import sys
import re
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import numpy as np
import math

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

x = [0.41,0.57,1.55,9.23,14.90,17.60]
y1 = [-51.1,-57.36,-66,-75.19,-82.43,-85.4]
y2 = [ 0,0,0,0,11,6]

xdata = np.asarray(x)
ydata = np.asarray(y1)
def Gauss(x, A, B):
    y = -A*(1/((x)**2))+B
    return y

parameters, covariance = curve_fit(Gauss, xdata, ydata)
fit_A = parameters[0]
fit_B = parameters[1]
fit_y = Gauss(xdata, fit_A, fit_B)

fig, ax = plt.subplots()

ax2 = ax.twinx()
ax2.bar(x, y2,label="Tx-Rx" , color = "blue", alpha=.2)
#ax2.bar(range(1,1+len(x)), packet_missing,label="packet missing" , color = "red", alpha=.2)
ax2.set_ylim(0, max(y2) * 2)

ax.plot(x,y1,"o",label="avg. RSSI", color= "green")
#ax.plot(xdata,fit_y,"--", color= "green")

# Value using the following equation:
#
x2 =10 ** (((-62.24250289) -(ydata))/(10 * 2))
x3 = [((-75)-(10*2)*math.log(l/9.23)) for l in xdata]
ax.plot(xdata,x3,"--", color= "red", label= "Expected values using equation 1")



ax.plot(x2,ydata,"--", color= "green", label= "Expected values using equation 2")
#ax.plot(range(1,1+len(rssi_values_parent)),rssi_values_server,label="server RSSI",color= "red")

ax.set_zorder(ax2.get_zorder()+1)
ax.set_frame_on(False)

ax.set_xticks(range(0,21))
ax.set_xlabel("Distance from server to client, Meters")
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
