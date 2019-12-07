import utime
import network
import config


def connect_wifi():
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASS)
        while(sta_if.isconnected() != True):
            utime.sleep(0.025)
        print("WiFi connection established")


if __name__ == "__main__":
    connect_wifi()