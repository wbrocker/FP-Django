# This Utils file it to interact with the Camera API's
from django.shortcuts import get_object_or_404
import requests
import json

from .models import ActiveCamera, ActiveDevices

def getCameraSettings(id):
    """
    Call the API for the camera based on id.
    This will update the DB with all the latest
    settings that are saved.
    """
    # instance = ActiveCamera.objects.get(pk=id)
    instance = ActiveDevices.objects.get(pk=id)
    ip_addr = instance.ip
    active = False
    # Load JSON
    data_dict = instance.data

    # Ensure the connection is handled if camera is
    # no available at the specified IP.
    try:
        r = requests.get('http://' + ip_addr + '/getstatus')
        result = r.content.decode('utf-8')
        result_json = json.loads(result)

        data_dict["flash"] = result_json['flash']
        data_dict["picinterval"] = result_json['picInterval']
        data_dict["firmwre"] = result_json['firmware']
        if result_json['camStatus'] == 1:
            instance.status = "ACT"
        elif result_json['camStatus'] == 0:
            instance.status = "INA"

        instance.save()
        active = True

    except:
        print("Error Connecting to Camera!")
        instance.status = "ERR"
        active = False

        instance.save()
    return active


def setCameraSettings(id):
    """ 
    Function to set the camera settings according
    to what was saved in the DB.
    """
    # cam = ActiveCamera.objects.get(id=id)
    cam = ActiveDevices.objects.get(id=id)
    # Read the JSON
    data_dict = cam.data

    # Ensure the mapping is correct.
    if cam.status == 'ACT':
        camStatus = 1
    else: 
        camStatus = 0

    # Define URL for Device
    url = "http://" + cam.ip + "/setdata"

    payload = data_dict

    # payload = {
    #     "flash": instance.device_flash,
    #     "picInterval": instance.device_picinterval,
    #     "camStatus": camStatus
    # }
    try:
        response = requests.post(url, json=payload)
    except:
        print("Error connecting to Camera!")
        cam.status = "ERR"
        cam.save()


    
