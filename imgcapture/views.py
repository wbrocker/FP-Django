import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from django.views.decorators.csrf import csrf_exempt
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import detect
from audit.utils import Audit
from alarm.models import AlarmConfig

import logging

from .forms import ImageForm
from .models import ImageDetection

# Function to re-analyze picture
def re_analyze(request, pk):
    # Retrieve the DB Object
    Audit("TEN", "Re-analyze image " + str(pk), "IMGCapture")
    image = get_object_or_404(ImageDetection, pk=pk)

    detect(image.id, './imgcapture/efficientdet_lite0.tflite')

    return redirect('dashboard:image', pk=pk)


def delete_image(request, pk):
    """
    Function to delete a specific image.
    """

    page = request.session.get('page_number', 1)
    # print("Page Number: " + str(page))

    Audit("IMA", "Deleting image: " + str(pk), "IMGCapture")
    # Retrieve the database object
    image = get_object_or_404(ImageDetection, pk=pk)

    # Get the filepath
    image_path = image.image.path

    # Delete the DB Object
    if image.dnd == False:
        image.delete()

        # Remove the file from storage as well.
        if os.path.exists(image_path):
            os.remove(image_path)

    # Construct the URL that include a page number
    url = reverse('dashboard:image-list') + '?' + urlencode({'page': page})

    return redirect(url)

def delete_all(request):
    """
    Delete all images apart from 
    the pictures marked as DND
    """
    alarm = AlarmConfig.objects.get(pk=1)
    Audit("IMA", "Deleting ALL images from Database", "IMGCapture")
    images_to_delete = ImageDetection.objects.filter(dnd=False)

    if request.method == 'POST':

        # Delete images one at a time
        for image in images_to_delete:
            image.image.delete()                # Delete the image from storage
            image.delete()                      # Delete the image form the DB

        return redirect('dashboard:image-list')
    
    else:
        return render(request, 'imgcapture/del_all.html',
                      {
                          'alarm': alarm
                      })

    


# csrf exempt to ensure easier upload from the ESP32-Cam
@csrf_exempt
def upload_image_view(request):

    # Confirm if it was a POST
    if request.method == 'POST':

        form = ImageForm(request.POST, request.FILES)

        logger = logging.getLogger(__name__)
        logger.debug(request.POST)
        logger.debug(request.FILES)
        print(request.POST)
   

        if form.is_valid():
            image_file = form.cleaned_data['image']
            instance = form.save()                      # Save the form instance to get the DB Record

            # Process the Detect function Asynchronously.
            detect(instance.id, './imgcapture/efficientdet_lite0.tflite')

            return redirect('imgcapture:success')
        else:
            print("This form is not valid!")
            print(form.errors)

    else:
        form = ImageForm()

    print("Upload Done")
    Audit("IMA", "Image uploaded.", "Camera")
    return render(request, 'upload.html', {'form': form})


def dnd(request, pk):
    # Do not delete image toggle
    image = get_object_or_404(ImageDetection, pk=pk)
    if (image.dnd == False):
        image.dnd = True
    else:
        image.dnd = False

    image.save()
    return redirect('dashboard:image-list')

def success(request):
    return HttpResponse('Successfully uploaded!')

