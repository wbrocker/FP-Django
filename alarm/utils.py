from django.shortcuts import get_object_or_404
import json

from .models import AlarmConfig, DetectionObjects
from imgcapture.models import ImageDetection

def checkAlarm(imageId):
    """
    Function to check conditions and 
    raise alarm if they are met
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
        
        # Else go through the list to see if object is detected
        elif len(image.detection_data) > 10:
            json_data = json.loads(image.detection_data)
            print("Iterating....")

            for item in json_data['detections']:
                print(item)
                if detlist.count(item['categories'][0]['category_name']) and item['categories'][0]['score'] >= alarm.score:
                    print("Item Detected! Alarm to be raised!")
                    raiseAlarm = True

    if raiseAlarm:
        print("Raising the Alarm!")
        