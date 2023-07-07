from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import logging

from .forms import ImageForm
from .models import ImageDetection

# Function to delete specific images
def delete_image(request, pk):
    image = ImageDetection.objects.get(pk=pk)
    image.delete()

    return redirect('dashboard:image-list')

@csrf_exempt
def upload_image_view(request):
    if request.method == 'POST':

        form = ImageForm(request.POST, request.FILES)

        logger = logging.getLogger(__name__)
        logger.debug(request.POST)
        logger.debug(request.FILES)

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