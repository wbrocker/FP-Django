from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

from imgcapture.models import ImageDetection


def index(request):
    # return HttpResponse("Main Dashboard")

    return render(request, 'dash/home.html')


# Function to return all images captured.
def imageList(request):
    all_images = ImageDetection.objects.all().order_by('-created')
    paginator = Paginator(all_images, 20)                       # 10 Images per page
    page = request.GET.get('page')

    for image in all_images:
        detection_data = json.loads(image.detection_data)
        image.detection_data = detection_data

    try:
        images = paginator.page(page)
        
    except PageNotAnInteger:
        # Show the 1st page if page parameter is not an integer
        images = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, show the last one
        images = paginator.page(paginator.num_pages)
    
        # Parse the detection_data for each image
        # for image in images:
        #     detection_data = json.loads(image.detection_data)
        #     image.detection_data = detection_data               # Replace the detection_data field
        #                                                         # with parsed JSON

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

