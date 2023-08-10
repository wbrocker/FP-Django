# This Utils file it to interact with the Camera API's
from django.shortcuts import get_object_or_404
import requests
import json

from .models import ActiveDevices


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
        data_dict["firmware"] = result_json['firmware']
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
    print("Updating Camera!")
    cam = ActiveDevices.objects.get(id=id)
    # Read the JSON
    data_dict = cam.data

    # Ensure the mapping is correct.
    # camStatus should be sent in JSON, but stored
    # as status variable in DB.
    if cam.status == 'ACT':
        data_dict["camStatus"] = True 
    else: 
        data_dict["camStatus"] = False

    # Define URL for Device
    url = "http://" + cam.ip + "/setdata"

    payload = data_dict

    try:
        response = requests.post(url, json=payload)
    except:
        print("Error connecting to Camera!")
        cam.status = "ERR"
        cam.save()

def setDeviceSettings(id):
    """
    Set the settings from the DB
    """
    device = ActiveDevices.objects.get(id=id)

    # Read the JSON
    data_dict = device.data

    if device.status == 'ACT':
        data_dict

def ChangeCamStatus(status):
    """
    Change the Alarm.
    Status = On/Off
    Type = Audible, Visual or Both
    """
    devices = ActiveDevices.objects.filter(type=ActiveDevices.Type.CAM)

    for dev in devices:
        # Check if Camera
        if dev == ActiveDevices.Type.CAM:
            if status:
                dev.status = ActiveDevices.Status.ACTIVE
            else:
                dev.status = ActiveDevices.Status.INACTIVE

        dev.save()
        setCameraSettings(dev.id)

    return True

def ActivateOrDeactivateAlarm(status):
    """
    Activate or Deactivate All Alarms
    """
    print("In Activate/Deactivate")
    devices = ActiveDevices.objects.all()

    for dev in devices:
        # Check if it's a camera
        if dev.type == ActiveDevices.Type.CAM:
            print("Changing Camera Status")
            if status:
                dev.status = ActiveDevices.Status.ACTIVE
            else:
                dev.status = ActiveDevices.Status.INACTIVE

        dev.save()
        getCameraSettings(dev.id)

    return True
