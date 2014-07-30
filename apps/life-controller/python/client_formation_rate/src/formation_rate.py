# Importation des bibliotheques    
from PIL import Image, ImageFilter 
import colorsys 
import time
import os
import threading
from client_formation_rate import *
from client_OSC import *
from server_OSC import *
import random
import numpy
import matplotlib
import matplotlib.pyplot as plt
import io
#import matplotlib.cm as cm




class formation_rate(threading.Thread):


    def __init__(self,un_client):
        
        threading.Thread.__init__(self)
        self.client_TCP = un_client

        """Lock for start and stop image analysis"""
        
        self.lock = threading.Lock()

        
        self.msg = None

        self.Values = None



        # Coordinates for the cropped images
        self.coordinates_crop ={"FORMATION_RATE" :  [0,0,0,0]}
        
        """to change to set the reference value"""
        self.low_reference = 0
                                 
        """set to True if life_controller asked infomration"""
        self._formation_rate_asked = [threading.Lock(), False]
                
        self.read_config_crop_FORMATION_RATE()

        
        print ("Cropping coordinates : " + str(self.coordinates_crop))
        
        """reference image"""
        """no formation"""
        self.url_image_ref_0 = "image/image_ref_0.jpg"
        """full formation"""
        self.url_image_ref_100 = "image/image_ref_100.jpg"
        
        self.curve = []
        self.formation_rate = []
        self.formation_rate_smoothed = []
        self.smoothing_coef = 30
        self.pixel_len_line = 50
        self.pixel_len_column = 50
        
        self.width_crop = 0
        self.height_crop = 0

        self.k = 20
        self.diff = 5
        self.cont_method = True
        
        """initialisation"""
        self.reset()
        
        self.client_OSC = client_OSC(self, "localhost", 3333)
        self.server_OSC = server_OSC(self, "localhost", 3335)
        
       
        

    # Read the values of TOP level and LOW level for each BU
    def read_config_crop_FORMATION_RATE(self):
        print("read crop values")
        try : 
            file = open("config/config_crop_FORMATION_RATE.txt", "r")
            
    
            for ligne in file :
                """Take out the end symbols (\n)"""
                ligne = ligne.strip()
                """split on  ':' """
                list = ligne.split(":")    
                
                if list[0].strip() == "FORMATION_RATE" :
                    coord = list[1].split(",")
                    """covert in int """
                    coord[0] = int(coord[0].strip())
                    coord[1] = int(coord[1].strip())
                    coord[2] = int(coord[2].strip())
                    coord[3] = int(coord[3].strip())
                    
                    self.coordinates_crop[list[0].strip()] = coord
                    
                    self.width_crop = abs(self.coordinates_crop[list[0].strip()][0] - self.coordinates_crop[list[0].strip()][2])
                    self.height_crop = abs(self.coordinates_crop[list[0].strip()][1] - self.coordinates_crop[list[0].strip()][3])
                
                
            file.close()
            
        except Exception as e : 
            print(str(e))
            print ("no file : config/config_crop_SPECTRO.txt in the directory")
            
    

    # Crop an image with the coordinates a,b,c,d and save it in the outfile in argument     
    
    def image_cropping(self,path_image_to_treat,path_destination_name, coordinates_crop):

        im = Image.open(path_image_to_treat)

        an_image = im.crop(coordinates_crop)

        an_image.save(path_destination_name,"jpeg")
        
        return an_image

    def get_uniformed_data_from_image(self, url, crop) :
        image = Image.open(url)
        image = image.crop(crop)
        image = image.convert('L')
        image = image.filter(ImageFilter.GaussianBlur(radius = 3))
        if self.cont_method :
            uniformed_data_full_image = self.get_both_edges(image, self.k, self.diff)
        else :
            data_full_image = list(image.getdata())
            data_mean = numpy.mean(data_full_image)
            data_std = numpy.std(data_full_image)
            uniformed_data_full_image = []
            for i in data_full_image :
                i = ((i - data_mean)/data_std)
                uniformed_data_full_image.append(i)
        return uniformed_data_full_image

    
    def get_edges(self, data, k, diff):
        data_quant = []
        for i in range(len(data)-k) :
            if abs(data[i]-data[i+k]) > diff :
                data_quant.append(0)
            else :
                data_quant.append (255)
        for i in range(k):
            data_quant.append(0)
        return data_quant

    def get_both_edges(self, image, k, diff):
        image_hor = image
        image_vert = image
        image_full_cont = image
        hor_cont = self.get_edges(list(image_hor.getdata()), k, diff)
        image_vert = image_vert.rotate(90)
        vert_cont = self.get_edges(list(image_vert.getdata()), k, diff)
        image_vert.putdata(vert_cont)
        image_vert = image_vert.rotate(-90)
        vert_cont = list(image_vert.getdata())
        full_cont = []
        
        for i in range(len(vert_cont)) :
            if vert_cont[i] == 0 or hor_cont[i] == 0 :
                full_cont.append(0)
            else :
                full_cont.append(255)
        return full_cont

    def compare_uniformed_data(self, current_image_data, ref_image_data) :
        subtract_images_data = numpy.subtract(current_image_data, ref_image_data)
        return list(subtract_images_data)
        
    def compare_pixels_group(self, subtract_images_data) :
        group_pixels_all_lines = []
        group_pixels_all_columns = []
        nb_pixels_compared_column = int(self.width_crop/self.pixel_len_line)
        nb_pixels_compared_line = int(self.height_crop/self.pixel_len_column)
        for i in range(self.height_crop) :
            group_pixels_partial = []
            for j in range(nb_pixels_compared_column) :
                group_pixels_partial.append(sum(subtract_images_data[((j*self.pixel_len_line)+i*self.width_crop):(((j+1)*self.pixel_len_line)+i*self.width_crop)]))
            if type(subtract_images_data[((self.pixel_len_line*nb_pixels_compared_column)+i*self.width_crop):((i+1)*self.width_crop)]) != list :
                group_pixels_partial.append(subtract_images_data[((self.pixel_len_line*nb_pixels_compared_column)+i*self.width_crop):((i+1)*self.width_crop)])
            else : 
                group_pixels_partial.append(sum(subtract_images_data[((self.pixel_len_line*nb_pixels_compared_column)+i*self.width_crop):((i+1)*self.width_crop)]))
            group_pixels_all_lines.extend([group_pixels_partial])
        
        group_pixels_all_lines = numpy.matrix(group_pixels_all_lines)
        for i in range(nb_pixels_compared_line) :
            group_pixels_all_columns.append(abs(sum(group_pixels_all_lines[(i*self.pixel_len_column):((i+1)*self.pixel_len_column),:])))
        if (len(group_pixels_all_lines)-nb_pixels_compared_line*self.pixel_len_column) != 0 :
            group_pixels_all_columns.append(abs(sum(group_pixels_all_lines[(nb_pixels_compared_line*self.pixel_len_column):, :])))
        return(numpy.sum(group_pixels_all_columns))

    def convert_to_formation_rate (self, compared_data, initial_compared_data) :        
        return 100*(1 - float(compared_data)/float(initial_compared_data))

    def smooth_formation_rate(self) :
        self.formation_rate_smoothed = []
        for i in range(len(self.formation_rate)) :
            if i < self.smoothing_coef:
                tmp = []
                while i >= 0 :
                    tmp.append(self.formation_rate[i])
                    i = i-1
                self.formation_rate_smoothed.append(sum(tmp)/len(tmp))
            else :
                self.formation_rate_smoothed.append(sum(self.formation_rate[(i-self.smoothing_coef):(i+1)])/(self.smoothing_coef+1))
        return self.formation_rate_smoothed

    """UNUSED FUNCTION"""
    def save_data(self, file, data) :
        display = str(data) + "\n"
        file.write(display)
        file.flush()

    def show_steadily_curve(self) :
        plt.plot(self.formation_rate)
        plt.plot(self.formation_rate_smoothed)
        plt.savefig("current_formation_rate_fig/current_fig_2")

    """return the value of the image asked"""
    def formation_rate_mesure_percent(self, url) :
        
        self.lock.acquire()
        value = 0 
        try : 
            print("calcul formation")
            uniformed_data_current_image = self.get_uniformed_data_from_image(url, self.coordinates_crop["FORMATION_RATE"])
           
            
            img_comparison = self.compare_uniformed_data(uniformed_data_current_image, self.uniformed_data_ref_image)
            img_comparison_by_pixels_group = self.compare_pixels_group(img_comparison)
            self.curve.append(img_comparison_by_pixels_group)
            """if first value is the reference"""
            #print( self.curve[0])
            #self.formation_rate.append(self.convert_to_formation_rate(img_comparison_by_pixels_group, self.curve[0]))
            """if other value is the reference"""
            """set ref at the first image """
            
            self.formation_rate.append(self.convert_to_formation_rate(img_comparison_by_pixels_group, self.low_reference))
            self.formation_rate_smoothed = self.smooth_formation_rate()
            print(self.formation_rate_smoothed )
            value = int(self.formation_rate_smoothed[len(self.formation_rate_smoothed)-1])
            
        except Exception as e :
            print(e)
            
        self.lock.release()
        value = value*3
        print("value " + url + " : " + str(value))
        return value
    
    def formation_rate_mesure_brut(self, url) :
        
        self.lock.acquire()
        uniformed_data_current_image = self.get_uniformed_data_from_image(url, self.coordinates_crop["FORMATION_RATE"])
       
        
        img_comparison = self.compare_uniformed_data(uniformed_data_current_image, self.uniformed_data_ref_image)
        img_comparison_by_pixels_group = self.compare_pixels_group(img_comparison)
        self.lock.release()
        
        return img_comparison_by_pixels_group
        

    """reset the old value of formation rate"""
    def reset(self):
        self.read_config_crop_FORMATION_RATE()
        self.uniformed_data_ref_image = self.get_uniformed_data_from_image(self.url_image_ref_100, self.coordinates_crop["FORMATION_RATE"])
        self.low_reference = self.formation_rate_mesure_brut(self.url_image_ref_0)
        self.formation_rate = []
        self.formation_rate_smoothed = []
        
    

    """set _formation_rate_asked"""
    def set_formation_rate_asked(self, state):
        self._formation_rate_asked[0].acquire()
        self._formation_rate_asked[1] = state
        self._formation_rate_asked[0].release()
   
    def get_formation_rate_asked(self):
        self._formation_rate_asked[0].acquire()
        state = self._formation_rate_asked[1] 
        self._formation_rate_asked[0].release()
        return state
    """to start analysis"""
    def start_formation_rate(self):
        """reset the old value of formation"""
        self.reset()
        self.set_formation_rate_asked(True) 
        print ("start formation_rate")

    """to stop analysis"""
    def stop_formation_rate(self):
        self.set_formation_rate_asked(False) 
        print ("stop formation_rate")


