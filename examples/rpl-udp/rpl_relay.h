#define RADIO_OFFSET -17 //reduced radio strengh. Testing possible on smaller distances.
#define RELAY_DBM -70 // level used for predicate switch to relay
#define RELAY_WARNING RELAY_DBM + 15 //an early warning of decaying signal. Used to print its time to send a drone
#define RELAY_RETURN_RSSI RELAY_DBM + 2 //While the client is connected through a relay it checks is the server RSSI is below this value.