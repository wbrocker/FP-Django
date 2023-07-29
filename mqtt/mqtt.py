import paho.mqtt.client as mqtt
from django.conf import settings


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

    from devices.models import ActiveDevices

    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

    # Birth and Deatch Notificaitons
    prefix = 'esp/lwt/'
    prefixTemp = 'esp/temp/'
    prefixHum = 'esp/hum/'

    if (msg.topic.startswith(prefix)):
        deviceId = msg.topic[len(prefix):]
        # print("Device Used: " + deviceid)
        deviceDb = ActiveDevices.objects.get(pk=deviceId)
        
        payload = msg.payload.decode('utf-8')
        # print(payload)
        if payload == 'hello':
            deviceDb.status = ActiveDevices.Status.ACTIVE
            print("Set device to active")
        elif payload == 'bye':
            deviceDb.status = ActiveDevices.Status.INACTIVE
            print("Set device to Inactive")

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

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)