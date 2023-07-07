from django.shortcuts import render
from django.http import HttpResponse

from imgcapture.models import ImageDetection

def index(request):
    # return HttpResponse("Main Dashboard")

    return render(request, 'dash/home.html')

def imageList(request):
    images = ImageDetection.objects.all().order_by('-created')

    return render(request,
                  'dash/images.html',
                  {'images': images})