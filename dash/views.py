from django.shortcuts import render
from django.http import HttpResponse
import json

from imgcapture.models import ImageDetection


def index(request):
    # return HttpResponse("Main Dashboard")

    return render(request, 'dash/home.html')


# Function to return all images captured.
def imageList(request):
    images = ImageDetection.objects.all().order_by('-created')

    # Parse the detection_data for each image
    for image in images:
        detection_data = json.loads(image.detection_data)
        image.detection_data = detection_data               # Replace the detection_data field
                                                            # with parsed JSON

    return render(request,
                  'dash/images.html',
                  {'images': images})


# Function to return individual image.
def individualImage(request, pk):
    image = ImageDetection.objects.get(pk=pk)
    detection_data = json.loads(image.detection_data)
    image.detection_data = detection_data

    return render(request,
                  'dash/image.html',
                  {'image': image})

