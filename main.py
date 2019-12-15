import sys
import utime
import ujson
import network
from machine import Pin
from umqttsimple import MQTTClient

import config

class Device:
    sta_if = network.WLAN(network.STA_IF)
    pusher = Pin(config.GPIO_PUSHER, Pin.IN, Pin.PULL_UP)
    led = Pin(config.GPIO_LED, Pin.OUT)
    user_topic = b'/user/%s' % config.USER_ID

    focused = 0

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

        # MQTT messages handler
        self.mqtt_client.set_callback(self.on_mqtt_message)

        # Button press handler
        self.pusher.irq(trigger=Pin.IRQ_RISING, handler=self.on_button_press)       

    def wait_for_network(self):
        while (self.sta_if.isconnected() != True):
            utime.sleep(0.025)

    def mqtt_check_message(self):
        while (True):
                utime.sleep(0.025)
                self.mqtt_client.check_msg()
    
    def connect_mqtt(self):
        try:
            self.mqtt_client.connect()
            self.mqtt_client.subscribe(self.user_topic)
        except Exception as e:
            print(sys.print_exception(e))
        else:
            print("Connected to %s" % config.MQTT_ENDPOINT)

    def compile_mqtt_payload(self, user_id, status):
        return '{"userId":"%s","focused":%i}' % (user_id, status)

    def mqtt_publish_status(self, status):
        payload = self.compile_mqtt_payload(config.USER_ID, status)
        self.mqtt_client.publish('/status', payload)

    def set_status(self, status):
            self.focused = status
            self.led.value(status)

    def on_button_press(self, value):
        try:
            new_status = 0 if self.focused else 1
            self.set_status(new_status)
            self.mqtt_publish_status(new_status)
        except Exception as e:
            print(sys.print_exception(e))

    def on_mqtt_message(self, topic, message):
        try:
            if topic == self.user_topic:
                new_status = ujson.loads(message)['focused']
                self.set_status(new_status)
        except Exception as e:
            print(sys.print_exception(e))
            
    def run(self):
        try:
            # Wait for WiFi connectivity
            self.wait_for_network()

            # Connect to the MQTT server
            self.connect_mqtt()
        except Exception as e:
            print(sys.print_exception(e))
        else:
            self.mqtt_check_message()


if __name__ == "__main__":
    Device().run()