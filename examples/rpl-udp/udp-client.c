#include <inttypes.h>
#include <stdint.h>

#include "contiki.h"
#include "net/ipv6/simple-udp.h"
#include "net/netstack.h"
#include "net/routing/routing.h"
#include "net/routing/rpl-lite/rpl.h"
#include "random.h"
#include "sys/log.h"
#include "examples/rpl-udp/rpl_relay.h"

#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define WITH_SERVER_REPLY 1
#define UDP_CLIENT_PORT 8765
#define UDP_SERVER_PORT 5678

#define SEND_INTERVAL (2* CLOCK_SECOND)

static struct simple_udp_connection udp_conn;
static uint32_t rx_count = 0;

/*---------------------------------------------------------------------------*/
PROCESS(udp_client_process, "UDP client");
AUTOSTART_PROCESSES(&udp_client_process);
/*---------------------------------------------------------------------------*/
static void
udp_rx_callback(struct simple_udp_connection *c,
                const uip_ipaddr_t *sender_addr,
                uint16_t sender_port,
                const uip_ipaddr_t *receiver_addr,
                uint16_t receiver_port,
                const uint8_t *data,
                uint16_t datalen) {
    LOG_INFO("Received response '%.*s' from ", datalen, (char *)data);
    LOG_INFO_6ADDR(sender_addr);
#if LLSEC802154_CONF_ENABLED
    LOG_INFO_(" LLSEC LV:%d", uipbuf_get_attr(UIPBUF_ATTR_LLSEC_LEVEL));
#endif
    LOG_INFO_("\n");
    rx_count++;
}

static int automatic_relay_switch() {
    return NETSTACK_ROUTING.activate_relay("Client from function");
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_client_process, ev, data) {
    static struct etimer periodic_timer;
    static char str[32];
    uip_ipaddr_t dest_ipaddr;
    static uint32_t tx_count;
    static uint32_t missed_tx_count;
    PROCESS_BEGIN();
   
    /* Initialize UDP connection */
    simple_udp_register(&udp_conn, UDP_CLIENT_PORT, NULL,
                        UDP_SERVER_PORT, udp_rx_callback);

    etimer_set(&periodic_timer, random_rand() % SEND_INTERVAL);

    /* Set the transmission power level to -12 dBm */
    radio_value_t power_level;
    NETSTACK_RADIO.get_value(RADIO_PARAM_TXPOWER, &power_level);
    radio_value_t new_power_level = power_level + (radio_value_t) RADIO_OFFSET;
    NETSTACK_RADIO.set_value(RADIO_PARAM_TXPOWER, new_power_level);
    rpl_set_leaf_only(1);
    while (1) {
        PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

        if (NETSTACK_ROUTING.node_is_reachable() &&
            NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr)) {
            /* Print statistics every 10th TX (Changed to 1  ) */ 
            if (tx_count % 1 == 0) {
                LOG_WARN("Tx/Rx/MissedTx: %" PRIu32 "/%" PRIu32 "/%" PRIu32 "\n",
                         tx_count, rx_count, missed_tx_count);
                automatic_relay_switch()
            }
            /* Send to DAG root */
            LOG_INFO("(client) Sending request %" PRIu32 " to ", tx_count);
            LOG_INFO_6ADDR(&dest_ipaddr);
            LOG_INFO_("\n");
            snprintf(str, sizeof(str), "(client) hello %" PRIu32 "", tx_count);
            simple_udp_sendto(&udp_conn, str, strlen(str), &dest_ipaddr);
            tx_count++;
        } else {
            LOG_INFO("Not reachable yet\n");
            if (tx_count > 0) {
                missed_tx_count++;
            }
        }
        // get the current value of the radio strength
        radio_value_t power_level;
        NETSTACK_RADIO.get_value(RADIO_PARAM_TXPOWER, &power_level);
        /*Print current value of radio signal strength*/
         LOG_INFO("Radio signal strength: %d \n",power_level);

        /* Add some jitter */
        etimer_set(&periodic_timer, SEND_INTERVAL - CLOCK_SECOND + (random_rand() % (2 * CLOCK_SECOND)));
    }

    PROCESS_END();
}

/*---------------------------------------------------------------------------*/
