Log files:
When logging into an active CC2650 launchpad, some old data is sent to the console. This old data is taken care of in the scripts but is still present in the files.
The log files had to be manually fixed in some cases, as new lines were not inserted properly when the files were saved.
In experiment 4 test 2, an initial RSSI value for the server was not outputted.
To accomodate this, the prior RSSI value was repeated instead.
A initial packet stability measurement was removed in exp 4 test 3 to ensure consistency, 
as the accompanying RSSI value printout was corrupted.

Python scripts:
There are 3 python scripts, 2 for plotting and 1 for extracting RSSI and packet measurements.
plot experiment 1.py is used for experiment 1, plot_Rssi.py is used for experiments 3,4 and 5.
Lines for packet measurement are outcommented in the current plot_Rssi.py to accomodate experiments 4 and 5.

measurement extractor experiment 1.py was used for experiment 1 to get different measurements,
such as avg. RSSI and the correct final packet measurements. The avg. RSSI print is currently outcommented.

plot_Rssi.py and measurement extractor experiment 1.py are used through command line arguments, the argument being the name of the file analyzed. 
plot experiment 1.py has hardcoded values.