from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from . import views
from .models import Locations, ActiveDevices

from .forms import LocationForm, DeviceForm

from .utils import getCameraSettings, setCameraSettings

def index(request):

    return HttpResponse("Devices Page")


def deviceList(request):
    """
    View that will list all the available
    devices
    """

    # camera_devices = ActiveCamera.objects.all().order_by('id')
    all_devices = ActiveDevices.objects.all().order_by('type')

    return render(request,
                  'devices/devices.html',
                  {
                   'devices': all_devices
                   })

def DelDevice(request, pk):
    """
    Delete Device From DB
    """
    device = ActiveDevices.objects.get(id=pk)

    device.delete()

    return redirect('devices:device-home')


# Form to add Camera Device
def addCamera(request):

    if request.method == 'POST':
        form = ActiveCameraForm(request.POST)

        if form.is_valid():
            instance = form.save()

            return redirect('devices:device-home')
        
        else:
            print(form.errors)

    else:
        form = ActiveCameraForm()

    return render(request, 'devices/addcam.html', {'form': form})

def AddDevice(request):
    """
    Function to Add devices
    """
    if request.method == 'POST':
        form = DeviceForm(request.POST)

        if form.is_valid():
            instance = form.save()

            return redirect('devices:device-home')
        
        else:
            print(form.errors)

    else:
        form = DeviceForm()

    return render(request, 'devices/adddevice.html', {'form': form})

# Form to edit device
def EditCam(request, pk):
    # cam = get_object_or_404(ActiveCamera, id=pk)
    cam = get_object_or_404(ActiveDevices, id=pk)

    if request.method == 'GET':
        # context = {'form': ActiveCameraForm(instance=cam), 'id': pk}
        context = {'form': DeviceForm(instance=cam), 'id': pk}
        return render(request, 'devices/editcam.html', context)
    
    elif request.method == 'POST':
        # form = ActiveCameraForm(request.POST, instance=cam)
        form = DeviceForm(request.POST, instance=cam)
        if form.is_valid():
            form.save()

            # Here I need to call a function to update the Cam Settings!
            # getCameraSettings(pk)
            
            setCameraSettings(pk)
            return redirect('devices:device-home')
        else:
            return render(request, 'devices/editcam.html', {'form':form})
        
# form to Edit Devices
def EditDevice(request, pk):
    device = get_object_or_404(ActiveDevices, id=pk)

    if request.method == 'GET':
        form = DeviceForm(instance=device)

        context = {'form': form, 'id': pk}
        # context = {'form': DeviceForm(instance=device), 'id': pk}
        # form.fields['device.ip'].widget.attrs['readonly'] = True

        return render(request, 'devices/edit_device.html', context)
    
    elif request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        
        if form.is_valid():
            form.save()

            if device.type == 'CAM':
                setCameraSettings(pk)
                return redirect('devices:device-home')
            
        else:
            return render(request, 'devices/edit_device.html', {'form': form})

    return redirect('devices:device-home')
        
# Change the Camera status
def setCamStatus(request):
    if request.method == 'GET':
        device_id = request.GET.get('device')
        # cam = get_object_or_404(ActiveCamera, id=device_id)
        cam = get_object_or_404(ActiveDevices, id=device_id)
        update = False

        if cam.status == 'ACT':
            cam.status = 'INA'
            update = True

        elif cam.status == 'INA':
            cam.status = 'ACT'
            update = True
        
        elif cam.status == 'ERR' or cam.status == 'DIS':
            if getCameraSettings(device_id):
                print("Device is active")
                cam.status = 'ACT'
                update = True
            else:
                print("Cam is still inactive")
                # Cam NOT active, no need to update
                update = False

        cam.save()
        # Update the Camera with new settings if Cam Available
        if update:
            setCameraSettings(device_id)

    return redirect('devices:device-home')

def setDeviceStatus(request):
    if request.method == 'GET':
        device_id = request.GET.get('device')

        device = get_object_or_404(ActiveDevices, id=device_id)

        if device.type == 'SEN':
            if device.status == 'INA' or device.status == 'DIS' or device.status == 'ERR':
                device.status = 'ACT'
            elif device.status == 'ACT':
                device.status = 'INA'

        device.save()

        # Update the device with new settings
        setDeviceSettings(device_id)

    return redirect('devices-home')


# Change the Camera Flash
def setCamFlash(request):
    device_id = request.GET.get('device')
    cam = get_object_or_404(ActiveDevices, id=device_id)

    # Read JSON data
    data_dict = cam.data

    if data_dict["flash"] == True:
        data_dict["flash"] = False

    elif data_dict["flash"] == False:
        data_dict["flash"] = True

    cam.save()
    
    # Update the Camera
    setCameraSettings(device_id)

    return redirect('devices:device-home')


@csrf_exempt
def registerDevice(request):
    """
    Function to register new devices, or for existing
    devices to pull the recent configration.
    This Function will be called by the Devices, and 
    NOT from the Dash.
    """
    # Determine the IP and Hostname
    ip_addr = request.GET.get('ip')
    hostname = request.GET.get('host')
    type_value = request.GET.get('type')
    firmware = request.GET.get('firmware')

    data = ""
    # if request.GET.get('type') is not None:
    #     deviceType = request.GET.get('type')
    # else: 
    #    deviceType = "None" 

    # Determine if the object is in the DB, update the Firmware
    # and respond with the current config.
    try:
        device = ActiveDevices.objects.get(ip=ip_addr)
        print("Device Exists!")
        if device.data is None:
            return HttpResponse(json.dumps("{'Error':'JSON Error'}"))
        else:
            device.firmware = firmware

            # If it's a Camera, determine correct status
            if device.type == 'CAM':
                if device.status == 'INA':
                    device.data['camStatus'] = False
                elif device.status == 'ACT':
                    device.data['camStatus'] = True
            device.save()
        # If this exists, return the settings to the device.
        # return HttpResponse(json.dumps(device.data)) if device.data else None
        return JsonResponse(device.data)

    except ActiveDevices.DoesNotExist:
        # This new device does not exist in the DB. Create a new record.    
        location, created = Locations.objects.get_or_create(name="Unknown")
        
        if type_value == 'CAM':
            # Insert Defaults
            data_json = json.loads('{"cameraid": 2,"flash": false,"picInterval": 200,"camStatus": false,"firmware": "0.13","sleep": false}')

        elif type_value == 'SEN':
            data_json = json.loads('{"sensorid": "5", "alarm": "1"}')

        new_device = ActiveDevices(ip=ip_addr, 
                                   name=hostname, 
                                   type=type_value, 
                                   location=location, 
                                   status=ActiveDevices.Status.DISCOVERED,
                                   data=data_json,
                                   firmware=firmware)
        new_device.save()

    # return HttpResponse(json.dumps(data_json))
    response = JsonResponse(data_json)
    response['Content-Type'] = "application/json"

    return response 


def LocationList(request):
    """
    View to list locations / rooms / areas.
    """
    locations = Locations.objects.all()
    print(locations)
    return render(request,
                'devices/location_list.html',
                {'locations': locations})


def AddLocation(request):
    """
    Add Locations
    """
    if request.method == 'POST':
        form = LocationForm(request.POST)
    
        if form.is_valid():
            instance = form.save()
            return redirect('devices:locations')
        
        else:
            print(form.errors)

    else:
        form = LocationForm()

    return render(request, 'devices/addloc.html',
                  {'form': form})


def EditLocation(request, pk):
    """
    Edit Locations
    """
    location = get_object_or_404(Locations, pk=pk)

    if request.method == 'POST':
        loc_form = LocationForm(request.POST, instance=location)
        
        if loc_form.is_valid():
            loc_form.save()
            return redirect('devices:locations')
    else:
        loc_form = LocationForm(instance=location)
    
    return render(request, 
                    'devices/editloc.html',
                    {'form': loc_form})


def DeleteLocation(request, pk):
    """
    Delete Locations from DB
    """
    location = get_object_or_404(Locations, pk=pk)

    if request.method == 'POST':
        location.delete()
        return redirect('devices:locations')
    
    return render(request, 'devices/del_loc.html', {'location': location})