# Importation des bibliotheques
import Image 
import colorsys
#import numpy 
import time
#import pylab
#import io
#from operator import itemgetter
import os,sys
#from PIL.ExifTags import TAGS
#import matplotlib.pyplot as plt
import threading
from client_level_py2_V2 import *



class image_level_V2(threading.Thread):


	def __init__(self,un_client):

		threading.Thread.__init__(self)
		self.client = un_client

		self.end_analysis = False

		"""Lock for start and stop image analysis"""
		
		self.lock = threading.Lock()
		
		self.BU_level = ""

		#self.Values = open("/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/les_mesures.txt","w")

		self.archives = false

		# Point of the calibrated image considered as the top
		self.top = 200

		# Point of the calibrated image considered as the bottom
		self.bottom = 100

#ce sont les limites le limage
	
	def image_cropping(image_a_traiter,outfile,a,b,c,d):

		im = Image.open(image_a_traiter)

		uneImage = im.crop((a,b,c,d))

		uneImage.save(outfile,"jpeg")



	def level_mesure(self,image_a_tester):

		#Detecte le niveau de rouge d'une image pour sortir le niveau de liquide
		im = Image.open(image_a_tester)  #Import the image 
		width,height = im.size

		calibrated_height = self.top - self.bottom

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

		for i in xrange(0,calibrated_height*width,pas):
			u = colorsys.rgb_to_hls(rouge[i]/255.0,vert[i]/255.0,bleu[i]/255.0)
			

			
			if ((u[1]< 0.7) & (u[1]>0.1) & (u[0]>0.9 or u[0]<0.1)& (u[2]>0.025)):   #Calibrates the color red selected
				color.append([i%width,(i-i%width)/width,u[0]])
				somme_pixels = somme_pixels + 1    
				
			
			if ( ((i)%width) > (((i+pas))%width) ):
				vecteur_pixels.append(somme_pixels)
				somme_pixels=0
			

		position_max = vecteur_pixels.index(max(vecteur_pixels))

		"""pourcentage_niveau = (float(height)-float(position_max))/float(height)
		pourcentage_niveau = round(pourcentage_niveau,4)"""
		#print  "\n"+ "niveau de remplissage :" + str(float(pourcentage_niveau)) + "%" +"\n"
		vecteur_pixels2 = []

		for i in xrange(len(vecteur_pixels)):
			if (vecteur_pixels[i]< (float(max(vecteur_pixels))/2)):
				vecteur_pixels2.append(0)
			else:
				vecteur_pixels2.append(vecteur_pixels[i])
		

		#Compteur de pics
		nb_pics = 0
		valeur_courante = 0
		vec_pics = []
		longueur_pic = 0
		centre_pic = 0

		for i in xrange(len(vecteur_pixels2)):
			if (i+1 == len(vecteur_pixels2)):
				if (vecteur_pixels2[i] != 0):
					vec_pics.append([nb_pics,longueur_pic,(i+i-float(longueur_pic))/2])

			else:
				if (vecteur_pixels2[i]== 0):
					if (vecteur_pixels[i+1] != 0):
						nb_pics +=1

				if (vecteur_pixels2[i] != 0):

					if(vecteur_pixels2[i+1]!=0):
						longueur_pic +=1

					if(vecteur_pixels2[i+1] == 0):
						vec_pics.append([nb_pics,longueur_pic,(i+i-float(longueur_pic))/2])
						longueur_pic = 0

		#on recupere que les pics qui sont larges de 2 pixels et plus
		vec_pics2 = []
		for i in xrange(len(vec_pics)):
			if (vec_pics[i][1]>0):
				vec_pics2.append(vec_pics[i])



		"""print "l'ensemble des pics :" + str(vec_pics2)
		#niveau_moyenne = float(ordonnee)/float(nb_pixels)

		outfile = image_a_tester
		fig2 = plt.figure()
		plt.grid(True)
		plt.plot(vecteur_pixels2)
		plt.show()"""


		le_centre = 0
		somme_longueur = 0


		for i in xrange(len(vec_pics2)):
			le_centre = le_centre + float(vec_pics2[i][1])*vec_pics2[i][2]
			somme_longueur += vec_pics2[i][1]

		

		if somme_longueur != 0 :
			le_centre = le_centre/(float(somme_longueur))
			#print "le barycentre est :" + str(le_centre)


			#return pourcentage_niveau
			pourcentage_niveau = (float(calibrated_height)-float(le_centre))/float(calibrated_height)
			pourcentage_niveau = round(pourcentage_niveau,4) 


			return pourcentage_niveau
		else:

			print "no red has been detected"
			return "null"


	def run(self):
		

		while True:


			self.lock.acquire()
			print "Start image analysis"

			# Ecrire le nom du path ou seront enregistrees les photos
			PathToFile = ""

			#os.system("streamer -s 1920x1080 -f jpeg -c /dev/video2 -b 16 -o ~/python_ws/Scripts_WorkShop_Avril/Test_Niveau//im_BU_level.jpeg")
			#os.system("streamer -s 1920x1080 -f jpeg -c /dev/video3 -b 16 -o ~/python_ws/Scripts_WorkShop_Avril/Test_Niveau/im_BR_level.jpeg")
			

			# Camera names (use imagesnap -l to identify)
			camera1 = "\"HD Pro Webcam C920\""
			camera2 = "\"HD Pro Webcam C920 #2\""
		
			os.system("imagesnap -d " + camera1 + " " + PathToFile + "im_BU_level.jpeg")
			os.system("imagesnap -d " + camera2 + " " + PathToFile + "im_BR_level.jpeg")


			time.sleep(1)


			#Changer le nom des paths

			#Path jusqu'a l'image a cropper 
			image_BU = PathToFile + "im_BU_level.jpeg"
			image_BR = PathToFile + "im_BR_level.jpeg"

			#Path jusqu'au dossier ou les sous-images seront sauvegardees
			PathToFile_croppedImages = PathToFile

			outfile_BR1 = PathToFile_croppedImages + "BR1.jpeg"
			outfile_BR2 = PathToFile_croppedImages + "BR2.jpeg"
			outfile_BR3 = PathToFile_croppedImages + "BR3.jpeg"
			outfile_BU1 = PathToFile_croppedImages + "BU1.jpeg"
			outfile_BU2 = PathToFile_croppedImages + "BU2.jpeg"
			outfile_BU3 = PathToFile_croppedImages + "BU3.jpeg"
	
			# rentrer a la main les coordonnees a,b et c,d qui sont differents pour chacune des photos
			a = 10
			b = 10
			c = 50
			d = 50

			image_cropping(image_BR,outfile_BR1,237,246,610,795)
			image_cropping(image_BR,outfile_BR2,811,363,1152,799)
			image_cropping(image_BR,outfile_BR3,1321,364,1660,807)
	
			image_cropping(image_BU,outfile_BU1,211,375,552,792)
			image_cropping(image_BU,outfile_BU2,777,388,1087,795)
			image_cropping(image_BU,outfile_BU3,1330,385,1672,792)

			#
			imBU1 = Image.open(outfile_BU1)
			imBU2 = Image.open(outfile_BU2)
			imBU3 = Image.open(outfile_BU3)
			imBR1 = Image.open(outfile_BR1)
			imBR2 = Image.open(outfile_BR2)
			imBR3 = Image.open(outfile_BR3)


			#self.level_mesure("BR1.jpeg")

			self.BU_level = "BU1 : " + str(self.level_mesure("BU1.jpeg")) + " , BU2 : " + str(self.level_mesure("BU2.jpeg")) + " , BU3 : " + str(self.level_mesure("BU3.jpeg")) + " , BR1 : " + str(self.level_mesure("BR1.jpeg")) + " , BR2 : " + str(self.level_mesure("BR2.jpeg")) + " , BR3 : " + str(self.level_mesure("BR3.jpeg")) + "\n"

			print "message envoye :" + str(self.BU_level)

			#si l'on souhaite archiver les photos prises et les mesures effectuees, passer self.archives a True
			#et definir dans les attributs le fichier dans lequel doivent etre ecrites les mesures
			if self.archives :

				self.Values.write("Valeurs des niveaux, " + time.strftime('%d/%m/%y %H:%M',time.localtime()) + " :" +"\n" + self.BU_level)

				imBU1.save("/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Archives/BU1." + time.strftime('%H:%M:%S')  + ".jpeg")
				imBU2.save("/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Archives/BU2." + time.strftime('%H:%M:%S')  + ".jpeg")
				imBU3.save("/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Archives/BU3." + time.strftime('%H:%M:%S')  + ".jpeg")
				imBR1.save("/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Archives/BR1." + time.strftime('%H:%M:%S')  + ".jpeg")
				imBR2.save("/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Archives/BR2." + time.strftime('%H:%M:%S')  + ".jpeg")
				imBR3.save("/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Archives/BR3." + time.strftime('%H:%M:%S')  + ".jpeg")

				self.Values.flush()

			self.lock.release()

			if not self.client._send(self.BU_level) :
				self.lock.acquire()
				
			print "End image analysis"


"""if __name__ == '__main__':
    
	analyse_test = analyse_image()
	run"""
