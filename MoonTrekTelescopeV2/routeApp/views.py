import PIL
from django.shortcuts import render
# import requests
from .forms import MoonPostForm
from routeApp.models import MoonPost
from PIL import Image
import os
from cv2 import *

from .processing.imageProcedure import RoutedImageCapture
# Create your views here.

def displayView(request):


    capture = RoutedImageCapture ()

    roots = capture.processUserImage()

    processed_degree_data = capture.processDegreeData()

    my_dict = {
        'image_path' : roots[0],
        'image_path1': roots[1],
        'degree_data': processed_degree_data,
    }

    return render(request,'routeApp/display.html', context=my_dict)




def upload (request):
    if request.method == "POST":
        form = MoonPostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()  # saves to database
            #check the compression rate
            img = PIL.Image.open(MoonPost.objects.last().user_image)
            wid, hgt = img.size
            sizeOfImageBytes = os.path.getsize('/Users/nicolasojeda/Desktop/MoonTrekTelescopeV2/MoonTrekTelescopeV2/media/'+ str(MoonPost.objects.last().user_image))
            compRate = wid * hgt / sizeOfImageBytes
            # print (compRate)
            if compRate > 6:
                return retry(request) #image will not pass registration or is too blurry
            else:
            # now we go to the first page ?
                return displayView(request)
    else:
        form = MoonPostForm()

    my_form = {
        'upload_form' : form,
    }


    return render(request,'routeApp/upload.html', context= my_form)


def retry(request):

    return render(request,'routeApp/retry.html', context={ })




def index(request):

    return render(request,'routeApp/index.html', context = { })

def display3DModel(request):

    model_dic= {

    }
    return render(request, "routeApp/generic3Dmodel.html", context=model_dic)












# def upload(request):
#     if request.method=="POST":
#         form = CaptureForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()  # saves to database
#
#             # EXIF CODE - need to add code to analyze the EXIF data
#             img_file = form.cleaned_data['image']
#
#             # address = extractAddress(img_file)
#             time = extractTime(img_file)
#             coordinates = extractCoordinates(img_file)
#             lon = extractLongitude(img_file)
#             lat = extractLatitude(img_file)
#
#             #If there is coordinates data and time
#             if (bool(coordinates) and bool(time)):
#                 return chooseCall(request,lon,lat,time)
#             #If there is missing data
#             else:
#                 return verify(request)  # The goal is at the end to send the user to verify page, for verification regardless if image had gps location , or it had exif data.
#
#
#     else:
#         form = CaptureForm()
#
#     my_form = {
#         'form': form
#     }
#     return render(request, "upload/upload.html", context=my_form)