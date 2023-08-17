import json

from .models import AlarmConfig, DetectionObjects
from imgcapture.models import ImageDetection
from devices.utils import GetSensorLocation
from audit.utils import Audit
from mqtt.mqtt import client as mqtt_client

def checkAlarm(imageId):
    """
    Function to check conditions and 
    raise alarm if they are met using the 
    picture id passed.
    """
    raiseAlarm = False 

    alarm = AlarmConfig.objects.first()
    detectObjects = DetectionObjects.objects.all()

    detlist = []        ## List that contains detectable objects.


    # Check if the alarm is set to On...
    if (alarm.status == 'ON'):
        image = ImageDetection.objects.get(pk=imageId)
        
        # Load items in the list.
        for item in detectObjects:
            if item.name == all and item.alarm_on_object:
                # Alarm on Any movement
                detlist.append('all')
        
            elif item.alarm_on_object and detlist.count('all') == 0:
                detlist.append(item.name)
        
        print("Detection Objects")
        print(detlist)

        # First check if the "ALL" alarm condition exists.
        if detlist.count('all') == 1:
            print("ALL Condition met for Alarm!")
            raiseAlarm = True
            Audit("ALA", "Alarm raised for movement", "Alarm")
        
        # Else go through the list to see if object is detected
        elif len(image.detection_data) > 10:
            json_data = json.loads(image.detection_data)
            print("Iterating....")

            for item in json_data['detections']:
                print(item)
                if detlist.count(item['categories'][0]['category_name']) and item['categories'][0]['score'] >= alarm.score:
                    print("Object Detected and Score is high! Alarm to be raised!")
                    raiseAlarm = True
                    desc = "Alarm for " + item['categories'][0]['category_name'] + " Score: " + str(item['categories'][0]['score']) + " > " + str(alarm.score)
                    Audit("ALA", desc, "Alarm")

        if raiseAlarm:
            print("Raising the Alarm!")
            # Write audit log
            alarm.current_type = alarm.type
            alarm.save()

def handleButton(clicks, sensor):
    """
    Function to handle the button clicks.
    """

    # Get sensor location
    location = GetSensorLocation(sensor)
    alarm = AlarmConfig.objects.first()
    alarm_status = alarm.current_type

    if clicks == '1':
        if alarm_status == AlarmConfig.ALARM_TYPES.OFF:     # Alarm is off. Just log
            print("Single Click while alarm is Off - " + location)
            Audit("ALA", "Button Clicked in " + location, "MQTT")
        else:
            # Acknowledge alarm.
            # Turn it off and write to Audit DB
            print("Turning Alarm off by Button Ack in " + location)
            alarm.current_type = AlarmConfig.ALARM_TYPES.OFF
            Audit("ALA", "Alarm disabled by button click from " + location, "MQTT")


    elif clicks == '2':
        # Double Click --> Raise Panic Alarm
        alarm.current_type = AlarmConfig.type               # Raise the alarm
        Audit("ALA", "Panic Button Pressed! - " + location, "MQTT")
        # All cameras to take a picture
        Audit("ALA", "Panic Button initiated picture on all Cameras!", "MQTT")
        # print("Taking picture on all cameras:");
        rc, mid = mqtt_client.publish('takepic', 0)


    # Save the new alarm state
    alarm.save()

    return True