# import requests
from cv2 import *
import numpy as np
# import matplotlib.pyplot as plt
import operator
import os
import glob
from PIL import Image
import math

from routeApp.models import MoonPost

class RoutedImageCapture:

    def __init__(self):
        self.image_raw_root = MoonPost.objects.last().user_image #This gets the last placed image in database
        self.image_processed_root=''
        self.degree_data = { }

    def processUserImage(self):


        ## Circle Detection
        img = cv2.imread('media/'+ str(self.image_raw_root), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 0.5, 100, param1=420, param2=10)
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            x, y, radius = int(detected_circles[0][0][0]), int(detected_circles[0][0][1]), int(
                detected_circles[0][0][2])
            center = (x, y)
        hight = img.shape[0]
        width = img.shape[1]

        #crop image

        yStart = y - radius
        if (yStart < 0):
            yStart = 0
        yEnd = y + radius
        if (yEnd > hight):
            yEnd = hight
        xStart = x - radius
        if (xStart < 0):
            xStart = 0
        xEnd = x + radius
        if (xEnd > width):
            xEnd = width


        croppedImg = img[yStart:yEnd, xStart:xEnd]

        # add pixels to the image
        top = y - radius
        if (top >= 0):
            top = 0
        if (top < 0):
            top = - (top)
        bottom = y + radius
        if (bottom <= hight):
            bottom = 0
        if (bottom > hight):
            bottom = (bottom - hight)
        left = x - radius
        if (left >= 0):
            left = 0
        if (left < 0):
            left = -(left)

        right = x + radius
        if (right <= width):
            right = 0
        if (right > width):
            right = right - width
        newImg = cv2.copyMakeBorder(croppedImg, top, bottom, left, right, cv2.BORDER_CONSTANT)



        # Produce a downsampled version of Globe Map

        ppd = round(newImg.shape[1] / 360)
        if (ppd <= 5):
            map = cv2.imread('static/globe_all/05_LRO_ref.jpg')

        if (ppd <= 7):
            map = cv2.imread('static/globe_all/07_LRO_ref.jpg')

        if (ppd <= 10):
            map = cv2.imread('static/globe_all/10_LRO_ref.jpg')

        if (ppd <= 15):
            map = cv2.imread('static/globe_all/15_LRO_ref.jpg')

        if (ppd <= 20):
            map = cv2.imread('static/globe_all/20_LRO_ref.jpg')
        # resize the map
        newMap = cv2.resize(map, (newImg.shape[1], newImg.shape[0]))

        print("H and W for new map", newImg.shape[0], newImg.shape[1])

        print("shape of new map", newMap.shape)

        # image regestration features matching (SIFT)
        imgGray = cv2.cvtColor(newImg, cv2.COLOR_BGR2GRAY)
        newMapGray = cv2.cvtColor(newMap, cv2.COLOR_BGR2GRAY)
        sift = cv2.xfeatures2d.SIFT_create()
        keypoints1, descriptors1 = sift.detectAndCompute(imgGray, None)
        keypoints2, descriptors2 = sift.detectAndCompute(newMapGray, None)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptors1, descriptors2, k=2)
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append([m])
        imMatches = cv2.drawMatchesKnn(newImg, keypoints1, newMap, keypoints2, good_matches, None,
                                       flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        # cv2_imshow(imMatches)

        cv2.waitKey(0)

        result = cv2.imwrite(
            'static/user_to_globe_registration/registration.png',
            imMatches)
        if result == True:
            print("File saved successfully")
        else:
            print("Error in saving file")

        user_to_globe_root = 'user_to_globe_registration/registration.png'

        #Warp image section
        # image regestration SIFT
        ref_matched_kpts = np.float32([keypoints1[m[0].queryIdx].pt for m in good_matches])
        sensed_matched_kpts = np.float32([keypoints2[m[0].trainIdx].pt for m in good_matches])

        # Compute homography
        H, status = cv2.findHomography(ref_matched_kpts, sensed_matched_kpts, cv2.RANSAC, 5.0)

        # Warp image
        imgAfterRegistration = cv2.warpPerspective(newImg, H, (newMapGray.shape[0], newMapGray.shape[1]))

        # save processed image
        result = cv2.imwrite(
            'static/user_images_processed/processed.jpg',
            imgAfterRegistration)
        if result == True:
            print("File saved successfully")
        else:
            print("Error in saving file")

        cv2.waitKey(3)

        self.image_processed_root = 'user_images_processed/processed.jpg'

        roots= [self.image_processed_root , user_to_globe_root]
        # some code here to process the WAC to be able to be used later in our 3D model
        # what needs to be processed is to cut it in the edges
        # once is cut and processed save the image in the folder static/WAC_resized/
        self.map_resize()

        return roots

    # def process_reference_image(self):
    #     #resize reference image
    #     #produce a downsampled version of globe
    #     #save downsampled version
    # def perform_registration(self):
    #     #now that you haave an accurate processed user image and a reference image perform registration
    #




#########################################################################################
    def map_resize(self):



        return None
    def processDegreeData(self):

        #some code here to acquire the right degree data
        #Procedure is as follows :
            #First need to get time of user image
        time = self.getTime()
            #second we wull need to get somehow lat , long
        lat = self.getLat()
        long = self.getLon()
        time = '2019-10-07T01:10:45' #lets assume this is the time for now since our function is not implemented
        lat = '113.5' #lets assume this is the lat for now since our function is not implemented
        lon = '34.0' #lets assume this is the lon for now since our function is not implemented


            #After obtaining the initial data then we can proceed to do JPL calls Vector , and Surface Point

                # calculate vector data
        bodies_position_vector = self.planetVectorAPICall(time)
                # calculate nearest point data
        earth_nearest_point_data = self.nearestPointAPICall(lon,lat,time)
                # calculate latitude to rectangular coordinates
        earth_rectangular_coordinates = self.latitudeToRectangular(lon,lat,time)

        # print(bodies_position_vector)
        # print(earth_nearest_point_data)
        # print(earth_rectangular_coordinates)


            # After this we will have the correct vector and Surface data that will allow us to start with our 3d model

                # send the data to a 3d model method that will be in charge of producing a 3d snapchot and save it to our static files

        self.model_3d(bodies_position_vector,earth_nearest_point_data,earth_rectangular_coordinates)

            # After above^ we should have our snapshot of the moon in 3d and now we can perform registration

        # in a method for registration , perform registration on the image and save the registration image in our static files as reference
        self.user_to_globe_registration()

        # we should have the degree data  calculated from user_to_globe_registration
        self.degree_data = {

            'xmin' : '%3A-87.14624379846742%2C',
            'ymin' :'%3A12.9515631722422%2C',
            'xmax' :'%3A-85.23182031292131%2C',
            'ymax' :'%3A14.865986657788309%2C',


        }
        return self.degree_data

    def getTime(self):
        return ''
    def getLat(self):
        return ''
    def getLon(self):
        return ''

    def planetVectorAPICall(self,time):
        # time needs to be converted into the correct format, like below
        # time = '2019-10-07T01:10:45'

        # making a get request to Moon Trek Portal for planet vector search where origin is earth

        # r = requests.get('https://trek.nasa.gov/los/planet-vector-search/moon/earth/' + time)
        #
        # json_object = r.json()
        # # print(json_object['positions']['earth'])
        #
        # # saving the obtained data in a dictionary
        # vector_dic = json_object['positions']['earth']

        return

    def nearestPointAPICall(self, lon, lat, time):
        # At this point lon and lat are recieved in the correct format
        # time needs to be converted into the correct format, like below
        # time = '2019-10-07T01:10:45'

        # making a get request to Moon Trek Portal for planet vector search where origin is earth
        # r = requests.get('https://trek.nasa.gov/los/nearest-point/earth/moon/' + lon + '/' + lat + '/' + time)
        #
        # json_object = r.json()
        # # print(type(json_object)) #just to test and print the contents of r to console , which should be the retrieved data
        #
        # # saving the obtained data in a dictionary
        # nearestPoint_dic = json_object

        return
    def latitudeToRectangular(self, lon, lat, time):
        # r = requests.get('https://trek.nasa.gov/los/lat-to-rect/earth/earth/' + lon + '/' + lat + '/' + time) # invalid request need to check with natalie
        # # json_object = r.json()
        # # latToRec_dic = json_object

        return 'latToRec_dic'

    def model_3d(self,bodies_position_vector , earth_nearest_point_data,earth_rectangular_coordinates):

        #this is where we need to produce an snapchot of an accurate 3d model of the moon
        # we either need to link to a threejs page do the whole procedure and then save the 'snapchot' into our static directory static/globe_3d_snapchot

        #lets assume we properly did the above procedure and now we have a 'snapchot' :) (for testing purposes)
        return None
    def user_to_globe_registration(self):

        #image registration team code goes here

            #images can be accessed from two folders ;
                # user image : can be found in static/user_images_processed
                # snapshot : can be found in static / globe_3d_snapshot

        #I guess main tasks for this method are ;
            #1. perform the most accurate registration with both images
            #2. produce an image registration image(the one with lines) and save it to static/usert_to_globe_registration
            #3. Lastly , The most important task , that can probably be implemented in another method would be to get the right degree data (pixel per degree)/ parameters


        return None

# el=esriSpatialRelIntersects&geometry=%7B"xmin"%3A-87.14624379846742%2C"ymin"%3A12.9515631722422%2C"xmax"%3A-85.23182031292131%2C"ymax"%3A14.865986657788309%2C"spatialReference"%3A%7B"wkid"%3A104903%7D%7D&geometryType=esriGeometryEnvelope&inSR=104903&outFields=*&outSR=104903