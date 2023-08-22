import paho.mqtt.client as mqtt
from django.conf import settings
import time

last_button_click_time = time.time()
debouce_period = 0.5

topic_last_message = {}

# Function for connecting
def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully!')
        mqtt_client.subscribe('#')
        mqtt_client.subscribe('alarms')             # Alarm Topic
        mqtt_client.subscribe('esp/#')              # All ESP's

    else:
        print('Bad connection. Code: ', rc)


# MQTT Function on receiving a message
def on_message(mqtt_client, userdata, msg):
    """
    This function is called when a message is received 
    from MQTT
    """
    from audit.utils import Audit
    from devices.models import ActiveDevices
    from devices.utils import GetSensorLocation

    # Birth and Deatch Notificaitons
    prefix = 'esp/lwt/'
    prefixTemp = 'esp/temp/'
    prefixHum = 'esp/hum/'
    prefixButton = 'esp/button/'

    # print("Topic: " + msg.topic + " ====== | Message: " + msg.payload.decode('utf-8'))

    if (msg.topic.startswith(prefix)):
        deviceId = msg.topic[len(prefix):]
        # print("Device Used: " + deviceid)
        deviceDb = ActiveDevices.objects.get(pk=deviceId)
        
        payload = msg.payload.decode('utf-8')
        # print(payload)
        if payload == 'hello':
            deviceDb.status = ActiveDevices.Status.ACTIVE
            print("Set device to active")
            auditMsg = "Sensor in " + GetSensorLocation(deviceId) + " is Active"
            Audit("SEN", auditMsg, "MQTT")
        elif payload == 'bye':
            deviceDb.status = ActiveDevices.Status.INACTIVE
            print("Set device to Inactive")
            auditMsg = "Sensor in " + GetSensorLocation(deviceId) + " is In-Active"
            Audit("SEN", auditMsg, "MQTT")

        print(deviceDb.status)
        deviceDb.save()
    
    # Temperature
    elif (msg.topic.startswith(prefixTemp)):
        deviceId = msg.topic[len(prefixTemp):]
        deviceDb = ActiveDevices.objects.get(pk=deviceId)
        payload = msg.payload.decode('utf-8')

        deviceDb.data['temperature'] = payload

        deviceDb.save()

    # Humidity
    elif (msg.topic.startswith(prefixHum)):
        deviceId = msg.topic[len(prefixHum):]
        deviceDb = ActiveDevices.objects.get(pk=deviceId)
        payload = msg.payload.decode('utf-8')

        deviceDb.data['humidity'] = payload

        deviceDb.save()

    # Button Clicks
    elif (msg.topic.startswith(prefixButton)):
        print("GOT THE BUTTON!")
        current_time = time.time()

        # if current_time - last_button_click_time >= debouce_period:
        # print(str(current_time - last_button_click_time))
        from alarm.utils import handleButton
        # print("MQTT TOPIC ESP/BUTTON/")
        # print("MQTT Button Clicked...............")

        deviceId = msg.topic[len(prefixButton):]
        print("DeviceID: " + deviceId)
        # deviceDb = ActiveDevices.objects.get(pk=deviceId)
        payload = msg.payload.decode('utf-8')
        print("Payload: " + payload)
        
        handleButton(payload, deviceId)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)