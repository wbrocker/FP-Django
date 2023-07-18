# This Utils file it to interact with the Camera API's
from django.shortcuts import get_object_or_404
import requests
import json

from .models import ActiveCamera

def getCameraSettings(id):
    """
    Call the API for the camera based on id.
    This will update the DB with all the latest
    settings that are saved.
    """
    instance = ActiveCamera.objects.get(pk=id)
    ip_addr = instance.device_ip

    # Ensure the connection is handled if camera is
    # no available at the specified IP.
    try:
        r = requests.get('http://' + ip_addr + '/getstatus')
        result = r.content.decode('utf-8')
        result_json = json.loads(result)

        instance.device_flash = result_json['flash']
        instance.device_picinterval = result_json['picInterval']
        instance.device_firmware = result_json['firmware']
        if result_json['camStatus'] == 1:
            instance.device_status = "Active"
        elif result_json['camStatus'] == 0:
            instance.device_status = "Inactive"

        instance.save()

    except:
        print("Error Connecting to Camera!")
        instance.device_status = "Error"

        instance.save()


def setCameraSettings(id):
    """ 
    Function to set the camera settings according
    to what was saved in the DB.
    """
    instance = ActiveCamera.objects.get(pk=id)

    # Ensure the mapping is correct.
    if instance.device_status == 'Active':
        camStatus = 1
    else: 
        camStatus = 0


    url = "http://" + instance.device_ip + "/setdata"

    payload = {
        "flash": instance.device_flash,
        "picInterval": instance.device_picinterval,
        "camStatus": camStatus
    }
    try:
        response = requests.post(url, json=payload)
    except:
        print("Error connecting to Camera!")
        instance.device_status = "Error"
        instance.save()


    
