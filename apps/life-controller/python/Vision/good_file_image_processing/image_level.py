# Importation des bibliotheques
from PIL import Image 
import colorsys
import numpy 
import time
import pylab
import io
from operator import itemgetter
import os,sys
from PIL.ExifTags import TAGS
import matplotlib.pyplot as plt
import threading
from client_level_py2 import *



class image_level(threading.Thread):


	def __init__(self,un_client):

		threading.Thread.__init__(self)
		self.client = un_client

		self.end_analysis = False

		"""Lock for start and stop image analysis"""
		
		self.lock = threading.Lock()
		
		self.BU_level = ""


	def level_mesure(self,image_a_tester):

		#Detecte le niveau de rouge d'une image pour sortir le niveau de liquide
		im = Image.open(image_a_tester)  #Import the image 
		width,height = im.size

		#Creation of three grey-scale maps red/green/blue
		r,g,b = im.split() 

		rouge = list(r.getdata())
		vert = list(g.getdata())
		bleu = list(b.getdata())

		# conversion RGB -> HSL
		h = []
		l = []
		s = []
		color = []

		vecteur_pixels = []
		somme_pixels = 0
		pas = 5

		for i in xrange(0,height*width,pas):
			u = colorsys.rgb_to_hls(rouge[i]/255.0,vert[i]/255.0,bleu[i]/255.0)
			

			
			if ((u[1]< 0.5) & (u[1]>0.1) & (u[0]>0.9 or u[0]<0.1)& (u[2]>0.1)):   #Calibrates the color red selected
				color.append([i%width,(i-i%width)/width,u[0]])
				somme_pixels = somme_pixels + 1    
				
			
			if ( ((i)%width) > (((i+pas))%width) ):
				vecteur_pixels.append(somme_pixels)
				somme_pixels=0
			

		position_max = vecteur_pixels.index(max(vecteur_pixels))

		pourcentage_niveau = (float(height)-float(position_max))/float(height)
		pourcentage_niveau = round(pourcentage_niveau,4)
		#print  "\n"+ "niveau de remplissage :" + str(float(pourcentage_niveau)) + "%" +"\n"
		return pourcentage_niveau


	def run(self):
		

		while not False:


			self.lock.acquire()
			print "Start image analysis"

			os.system("streamer -s 1920x1080 -f jpeg -c /dev/video1 -b 16 -o ~/python_ws/Scripts_Tests/Script_Bilan/Scripts_WorkShop_Avril/Test_Niveau/im_BU_level.jpeg")

			time.sleep(5)

			os.system("./decoupe2") #adapter la decoupe pour 1 buffer
			
			#for i in xrange(1,4):
			#mesureNiveau("flot"+ str(i) + ".jpg")
			#NiveauBuf.append(mesureNiveau("flot"+ str(i) + ".jpg"))
			
			self.level_mesure("buf1.jpeg")
			
			self.BU_level = "lvl_BU1:" + str(self.level_mesure("buf1.jpeg"))


			print self.BU_level
			self.client._send(self.BU_level)

			self.lock.release()
			print "End image analysis"


"""if __name__ == '__main__':
    
	analyse_test = analyse_image()
	run"""
