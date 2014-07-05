# Importation des bibliotheques	
from PIL import Image 
import colorsys 
import time
import os
import threading
from client_level import *
import random



class image_level(threading.Thread):


	def __init__(self,un_client):
		
		threading.Thread.__init__(self)
		self.client = un_client

		"""Lock for start and stop image analysis"""
		
		self.lock = threading.Lock()
		self.lock.acquire()
		
		self.msg = None
		
		


		
		self.archives = False
		self.Values = None
		if self.archives : 
			self.Values = open("les_mesures.txt","w")



		# Coordinates for the cropped images
		self.coordinates_crop ={"AQ" :  [0,0,0,0],\
                          		}


		# Dictionnaries that gather of TOP and LOW levels for calibration
		self.calibration_values = {'AQ':{'HIGH':0,'LOW':0}}
		
		self._level= { 	"AQ" :  0}
						
				
		self.read_config_crop_AQ()
		self.read_calibration_AQ()
		
		print ("Cropping coordinates : " + str(self.calibration_values))
		
		self.start()

	# Read the values of TOP level and LOW level for each BU
	def read_config_crop_AQ(self):
		print("read crop values")
		try : 
			file = open("config/config_crop_AQ.txt", "r")
			
	
			for ligne in file :
				"""Take out the end symbols (\n)"""
				ligne = ligne.strip()
				"""split on  ':' """
				list = ligne.split(":")	
				
				if list[0].strip() == "AQ" :
					coord = list[1].split(",")
					"""covert in int """
					coord[0] = int(coord[0].strip())
					coord[1] = int(coord[1].strip())
					coord[2] = int(coord[2].strip())
					coord[3] = int(coord[3].strip())
					
					self.coordinates_crop[list[0].strip()] = coord
					
					
			file.close()
			
		except Exception as e : 
			print(str(e))
			print ("no file : config/config_crop_SPECTRO.txt in the directory")
			
	

	# Read the coordinates for the image cropping of each BU 
	def read_calibration_AQ(self):

		the_file = open("config/config_calibration_AQ_HIGH.txt", "r")

		for ligne in the_file :
			"""Take out the end symbols space"""
			ligne = ligne.strip()


			"""split on  ':' """
			a_list = ligne.split(":")

			if a_list[0].strip() == "AQ":
				if a_list[1].strip() == "HIGH":
					self.calibration_values[a_list[0].strip()][a_list[1].strip()] = int(a_list[2].strip())


		# Fermeture du fichier
		the_file.close()
		
		the_file = open("config/config_calibration_AQ_LOW.txt", "r")

		for ligne in the_file :
			"""Take out the end symbols space"""
			ligne = ligne.strip()


			"""split on  ':' """
			a_list = ligne.split(":")

			if a_list[0].strip() == "AQ":
				if a_list[1].strip() == "LOW":
					self.calibration_values[a_list[0].strip()][a_list[1].strip()] = int(a_list[2].strip())
		# Fermeture du fichier
		the_file.close()


	# Crop an image with the coordinates a,b,c,d and save it in the outfile in argument 	
	
	def image_cropping(self,path_image_to_treat,path_destination_name, coordinates_crop):

		im = Image.open(path_image_to_treat)

		an_image = im.crop(coordinates_crop)

		an_image.save(path_destination_name,"jpeg")
		
		return an_image


	# Mesure the level
	
	"""take an image already cropped, with his container_name"""
	def level_mesure(self,image_a_tester,conteneur_name):

		top = self.calibration_values[conteneur_name]["HIGH"]
		bottom = self.calibration_values[conteneur_name]["LOW"]

		#im = Image.open(image_a_tester_name)  #Import the image 
		im = image_a_tester
		
		width,height = im.size


		calibrated_height = bottom - top

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

		for i in range(0,calibrated_height*width,pas):
			u = colorsys.rgb_to_hls(rouge[i]/255.0,vert[i]/255.0,bleu[i]/255.0)
			

			
			if ((u[1]< 0.7) & (u[1]>0.1) & (u[0]>0.9 or u[0]<0.1)& (u[2]>0.025)):   #Calibrates the color red selected
				color.append([i%width,(i-i%width)/width,u[0]])
				somme_pixels = somme_pixels + 1	
				
			
			if ( ((i)%width) > (((i+pas))%width) ):
				vecteur_pixels.append(somme_pixels)
				somme_pixels=0
			

		vecteur_pixels2 = []

		for i in range(len(vecteur_pixels)):
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

		for i in range(len(vecteur_pixels2)):
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
		for i in range(len(vec_pics)):
			if (vec_pics[i][1]>0):
				vec_pics2.append(vec_pics[i])



		le_centre = 0
		somme_longueur = 0


		for i in range(len(vec_pics2)):
			le_centre = le_centre + float(vec_pics2[i][1])*vec_pics2[i][2]
			somme_longueur += vec_pics2[i][1]

		
		return round(random.random(),2)
	
		"""if somme_longueur != 0 :
			le_centre = le_centre/(float(somme_longueur))


			#return pourcentage_niveau
			pourcentage_niveau = (float(calibrated_height)-float(le_centre))/float(calibrated_height)
			pourcentage_niveau = round(pourcentage_niveau,4) 

			#pourcentage_niveau = int(100*random.random())
			return pourcentage_niveau
		else:

			print("no red has been detected")
			return 'null'"""


	def run(self):


		#ne rentrer dans le while que si les coordonnees ne sont pas toutes nulles et si la calibration a ete faite?

		while True:


			self.lock.acquire()
			print("Start image analysis")

			# Ecrire le nom du path ou seront enregistrees les photos
			PathToFile = ""

			#os.system("streamer -s 1920x1080 -f jpeg -c /dev/video2 -b 16 -o ~/python_ws/Scripts_WorkShop_Avril/Test_Niveau//im_BU_level.jpeg")
			#os.system("streamer -s 1920x1080 -f jpeg -c /dev/video3 -b 16 -o ~/python_ws/Scripts_WorkShop_Avril/Test_Niveau/im_BR_level.jpeg")
			

			# Camera names (use imagesnap -l to identify)
			camera1 = "\"HD Pro Webcam C920\""
			#camera3 = "\"Built-in iSight\""
		
			os.system("imagesnap -d " + camera1 + " " + PathToFile + "im_AQ_level.jpeg")
			


			#time.sleep(1)


			#Path jusqu'a l'image a cropper 
			image_AQ = PathToFile + "im_AQ_level.jpeg"
			

			#Path jusqu'au dossier ou les sous-images seront sauvegardees
			PathToFile_croppedImages = PathToFile


			outfile_AQ = PathToFile_croppedImages + "AQ.jpeg"
			
	

			im_cropped_AQ = self.image_cropping(image_AQ,outfile_AQ,self.coordinates_crop["AQ"])
			
			self._level["AQ"] = self.level_mesure(im_cropped_AQ, "AQ")
			
			
			self.msg = str(self._level)
			self.msg = self.msg.replace("{", "")
			self.msg = self.msg.replace("}", "")
			self.msg = self.msg.replace("'", "")
			

			
			print("message envoye :" + self.msg)
			self.client._send(self.msg)
			#si l'on souhaite archiver les photos prises et les mesures effectuees, passer self.archives a True
			#et definir dans les attributs le fichier dans lequel doivent etre ecrites les mesures
			
			if self.archives :
				
				
				self.Values.write("Valeurs des niveaux, " + time.strftime('%d/%m/%y %H:%M',time.localtime()) + " :" +"\n" + self.msg)

				im_cropped_AQ.save("archives/AQ." + time.strftime('%H:%M:%S')  + ".jpeg")
				
				self.Values.flush()

			
			self.lock.release()

			if self._stop :
				self._stop_level()
				
			print("End image analysis")

	"""to start analysis"""
	def start_level(self):
		self._stop = False
		self.lock.release()
	"""to stop analysis"""
	def stop_level(self):
		self._stop = True
	"""do not use this function"""
	def _stop_level(self):
		self.lock.acquire()
