import sys
import utime
import network
from machine import Pin
from umqttsimple import MQTTClient

import config


class Device:
    sta_if = network.WLAN(network.STA_IF)
    pusher = Pin(config.GPIO_PUSHER, Pin.IN)
    led = Pin(config.GPIO_LED, Pin.OUT, value=Pin.PULL_UP)

    state = {
        "focused": False
    }

    def __init__(self):
        # Instantiate MQTT client
        self.mqtt_client = MQTTClient(
            client_id=config.DEVICE_ID,
            server=config.MQTT_ENDPOINT,
            port=config.MQTT_PORT,
            user=config.MQTT_USERNAME,
            password=config.MQTT_PASSWORD,
            keepalive = 10000,
        )

        # Button press handlers
        # self.pusher.irq(handler=self.on_pusher_press, trigger=Pin.IRQ_RISING)       

    def wait_for_network(self):
        while (self.sta_if.isconnected() != True):
            utime.sleep(0.025)
    
    def connect_mqtt(self):
        try:
            self.mqtt_client.connect()
        except Exception as e:
            print(sys.print_exception(e))
        else:
            print("Connected to %s" % config.MQTT_ENDPOINT)

    def run(self):
        try:
            # Wait for WiFi connectivity
            self.wait_for_network()

            # Connect to the MQTT server
            self.connect_mqtt()
        except Exception as e:
            print(sys.print_exception(e))
        else:
            while (True):
                utime.sleep(0.025)


if __name__ == "__main__":
    Device().run()