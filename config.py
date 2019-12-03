# WiFi configuration
WIFI_SSID = 'ivan-ap'
WIFI_PASS = 'iot-2019'

# GPIO mapping
GPIO_LED = 23
GPIO_PUSHER = 22

# AWS general configuration
AWS_PORT = 8883
AWS_HOST = 'a1bu9mvwtbkb8l-ats.iot.eu-west-3.amazonaws.com'
AWS_ROOT_CA = '/flash/cert/aws_root.pem.der'
AWS_CLIENT_CERT = '/flash/cert/aws_client.crt.der'
AWS_PRIVATE_KEY = '/flash/cert/aws_private.pem.der'

################## Subscribe / Publish client #################
CLIENT_ID = 'esp32-0001'
TOPIC = 'PublishTopic'
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5