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
    mqtt_client = MQTTClient(
        client_id = config.CLIENT_ID,
        server = config.AWS_HOST,
        port = config.AWS_PORT,
        keepalive = 10000,
        ssl = True,
        ssl_params = {
            "certfile": config.AWS_CLIENT_CERT, 
            "keyfile": config.AWS_PRIVATE_KEY, 
            "ca_certs": config.AWS_ROOT_CA,
        }
    )


    state = {
        "focused": False
    }


    # def __init__(self):
    #     # Button press handlers
    #     self.pusher.irq(handler=self.on_pusher_press, trigger=Pin.IRQ_RISING)        
            

    def connect_wifi(self):
        self.sta_if.active(True)
        self.sta_if.connect(config.WIFI_SSID, config.WIFI_PASS)
        while(self.sta_if.isconnected() != True):
            utime.sleep(0.025)
        return None

    
    def connect_aws(self):
        try:
            self.mqtt_client.connect()
        except Exception as e:
            print(e)
        else:
            print("Connected to AWS")


    def run(self):
        try:
            # Establish WiFi connection
            self.connect_wifi()
            # Establish connection with AWS
            self.connect_aws()
        except:
            sys.exit(1)
        else:
            while (True):
                utime.sleep(0.025)



if __name__ == "__main__":
    Device().run()