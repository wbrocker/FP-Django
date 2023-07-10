import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .utils import detect

import logging

from .forms import ImageForm
from .models import ImageDetection

# Function to delete specific images
def delete_image(request, pk):
    # Retrieve the database object
    image = get_object_or_404(ImageDetection, pk=pk)

    # Get the filepath
    image_path = image.image.path

    # Delete the DB Object
    image.delete()

    # Remove the file from storage as well.
    if os.path.exists(image_path):
        os.remove(image_path)

    return redirect('dashboard:image-list')


# csrf exempt to ensure easier upload from the ESP32-Cam
@csrf_exempt
def upload_image_view(request):
    # Confirm if it was a POST
    if request.method == 'POST':

        form = ImageForm(request.POST, request.FILES)

        logger = logging.getLogger(__name__)
        logger.debug(request.POST)
        logger.debug(request.FILES)

        print(request.FILES['image'])

        test = detect(request.FILES['image'], 'efficientdet_lite0.tflite')

        if form.is_valid():
            image_file = form.cleaned_data['image']
            form.save()
            return redirect('imgcapture:success')
        else:
            print("This form is not valid!")
            print(form.errors)

    else:
        form = ImageForm()

    return render(request, 'upload.html', {'form': form})

def success(request):
    return HttpResponse('Successfully uploaded!')