from django.shortcuts import render
from django.http import HttpResponse

from imgcapture.models import ImageDetection

def index(request):
    # return HttpResponse("Main Dashboard")

    return render(request, 'dash/home.html')


# Function to return all images captured.
def imageList(request):
    images = ImageDetection.objects.all().order_by('-created')

    return render(request,
                  'dash/images.html',
                  {'images': images})


# Function to return individual image.
def individualImage(request, pk):
    image = ImageDetection.objects.get(pk=pk)

    return render(request,
                  'dash/image.html',
                  {'image': image})