'''
Created on Jun 1, 2014

@author: Cactus
'''
# Importation des bibliotheques
from PIL import Image 
import numpy

class spectro_level(object):

    def __init__(self,un_window):
    
        self.window = un_window

        self.end_analysis = False

        
        self.concentration_value = ""

    """return the level concentration"""
    def get_level(self,image_full, name,  crop):
        self.image_cropping(image_full, name,crop[0], crop[1], crop[2], crop[3] )
        
        return self.absorption(name+".jpg") 
    # Crop a picture 

    def image_cropping(self, image_a_traiter,outfile,a,b,c,d):
        im = Image.open(image_a_traiter)

        uneImage = im.crop((a,b,c,d))
        
        uneImage.save(outfile+".jpg","jpeg")

    
    def absorption(self,image_a_traiter):
 
        mean = 0
        
        """open the image to treat, crop has been made before"""
        image_treated = Image.open(image_a_traiter)
        
        """convert in gray level ?"""
        #image_treated = image_treated.convert("L")
        
        """convert in list"""
        data=list(image_treated.getdata())
        """get the mean of the pixel"""
        
        mean = numpy.mean(data)


        return mean

