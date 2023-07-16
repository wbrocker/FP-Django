from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import views
from .models import ActiveCamera

from .forms import ActiveCameraForm

def index(request):

    return HttpResponse("Devices Page")


# Function to show devices
def deviceList(request):
    camera_devices = ActiveCamera.objects.all().order_by('id')

    return render(request,
                  'devices/devices.html',
                  {'cameras': camera_devices})


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