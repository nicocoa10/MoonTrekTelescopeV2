import requests

class ImageProcceses:

    def __init__(self):
        self.image_raw_root = 'MoonTrekTelescopeV2/media/user_images_raw/userMoon.png'
        self.image_processed_root=''
        self.degree_data = { }

    def processUserImage(self):

        #some code here to process the image
        # what needs to be processed is to cut it in the edges
        #once is cut and processed save the image in the folder static/user_images_processed/

        self.image_processed_root = 'user_images_processed/userMoon.png'

        return self.image_processed_root



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

        r = requests.get('https://trek.nasa.gov/los/planet-vector-search/moon/earth/' + time)

        json_object = r.json()
        # print(json_object['positions']['earth'])

        # saving the obtained data in a dictionary
        vector_dic = json_object['positions']['earth']

        return vector_dic

    def nearestPointAPICall(self, lon, lat, time):
        # At this point lon and lat are recieved in the correct format
        # time needs to be converted into the correct format, like below
        # time = '2019-10-07T01:10:45'

        # making a get request to Moon Trek Portal for planet vector search where origin is earth
        r = requests.get('https://trek.nasa.gov/los/nearest-point/earth/moon/' + lon + '/' + lat + '/' + time)

        json_object = r.json()
        # print(type(json_object)) #just to test and print the contents of r to console , which should be the retrieved data

        # saving the obtained data in a dictionary
        nearestPoint_dic = json_object

        return nearestPoint_dic
    def latitudeToRectangular(self, lon, lat, time):
        r = requests.get('https://trek.nasa.gov/los/lat-to-rect/earth/earth/' + lon + '/' + lat + '/' + time) # invalid request need to check with natalie
        # json_object = r.json()
        # latToRec_dic = json_object

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
            #3. Lastly , The most important task , that can probably be implemented in another method would be to get the right degree data (pixel per degree)


        return None

# el=esriSpatialRelIntersects&geometry=%7B"xmin"%3A-87.14624379846742%2C"ymin"%3A12.9515631722422%2C"xmax"%3A-85.23182031292131%2C"ymax"%3A14.865986657788309%2C"spatialReference"%3A%7B"wkid"%3A104903%7D%7D&geometryType=esriGeometryEnvelope&inSR=104903&outFields=*&outSR=104903