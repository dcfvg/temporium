# Importation des bibliotheques	
from PIL import Image , ImageFilter
import colorsys 
import time
import os
import threading
from client_level import *
import random
import numpy



class image_level(threading.Thread):


	def __init__(self,un_client):
		# define parameters for the level_mesure function. To know their role, go and check the comments of that function.
		self.k = 1
		self.diff = 5
		self.gaussian_radius = 2
		self.nb_pixel_level_line = 5

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

		# Camera names (use imagesnap -l to identify)
		self.camera_AQ = ""

		# Coordinates for the cropped images
		self.coordinates_crop ={"AQ" :  [0,0,0,0],\
							   }

		# Dictionnaries that gather of TOP and LOW levels for calibration
		self.calibration_values = {'AQ':{'HIGH':0,'LOW':0}}

		self._level= { 	"AQ" :  0}

		self.read_config_crop_AQ()
		self.read_calibration_AQ()
		self.read_config_camera()
		

		print ("Cropping coordinates : " + str(self.calibration_values))

		self.start()

	def read_config_camera(self):
		print("read config camera")
		try : 
			file = open("config/config_camera.txt", "r")
			
	
			for ligne in file :
				"""Take out the end symbols (\n)"""
				ligne = ligne.strip()
				"""split on  ':' """
				list = ligne.split(":")	
				
				if list[0].strip() == "AQ" :
					self.camera_AQ = "\"" + list[1].strip() +"\""
					
					
			file.close()
			
		except Exception as e : 
			print(str(e))
			print ("no file : config/config_camera.txt in the directory")
			
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

	# Detect the vertical edges of an image (the information about the level is vertical)
	# To detect the edges, it will copare two pixels in the same colum of the image.
	# k represent the distance between those two pixels.
	# diff represent the threshold after which the difference is taken into account
	# The function return the image which just the edges 
	def get_edges(self, image_a_traiter, k, diff):
		image = image_a_traiter.rotate(90)
		data = list(image.getdata())
		data_quant = []
		for i in range(len(data)-k) :
			if abs(data[i]-data[i+k]) > diff :
				data_quant.append(0)
			else :
				data_quant.append (255)
		for i in range(k):
			data_quant.append(0)
		image.putdata(data_quant)
		image = image.rotate(-90)
		"""uncomment to see analysed image"""
		#image.show()
		return image

	# Get the data of an image and put it in a list of lists, each list representing a line of the image
	# Take an image and return a list of lists

	def data_to_image (self, image) :
		image_width,image_height = image.size
		raw_data_full_image=list(image.getdata())
		data_full_image = []
		for i in range(image_height):
			data_pixel_line=[]
			for j in range(image_width):
				data_pixel_line.append(raw_data_full_image[i*image_width+j])
			data_full_image.append(data_pixel_line)
		return numpy.asarray(data_full_image)


	# Mesure the level
	# take an image already cropped, with his container_name
	# k and diff are parameters used for the function get_edges, see the comments about this function to know their role
	# as the image is filtred with a Gaussian type filter, gaussian_radius is the radius used to apply this filter
	# nb_pixel_level_line is the threshold after which a black line in an image wit edges will be considered a level

	def level_mesure(self,image_a_tester,conteneur_name):

		top = self.calibration_values[conteneur_name]["HIGH"]
		bottom = self.calibration_values[conteneur_name]["LOW"]

		#im = Image.open(image_a_tester_name)  #Import the image 
		im = image_a_tester

		width,height = im.size

		calibrated_height = bottom - top

		im = im.convert('L')
		im = im.filter(ImageFilter.GaussianBlur(radius = self.gaussian_radius))
		im = self.get_edges(im,self.k,self.diff)

		level = []
		im = im.rotate(90)
		data = self.data_to_image(im)
		for j in range(width) :
			for i in range(height - 5*self.nb_pixel_level_line) :
				if sum(data[j][i:i+self.nb_pixel_level_line]) == 0 :
					level.append(i+int(self.nb_pixel_level_line/2))

		if len(level) != 0 :

			#return pourcentage_niveau
			pourcentage_niveau = 1 - (float(numpy.mean(level)-top)/(bottom-top))
			#pourcentage_niveau = (1-float(numpy.mean(level))/float(calibrated_height))
			pourcentage_niveau = round(pourcentage_niveau,4)
 
			#pourcentage_niveau = int(100*random.random())
			return pourcentage_niveau
		else:
 
			print("no edges have been detected")
			return 'null'
	
	def run(self):


		#ne rentrer dans le while que si les coordonnees ne sont pas toutes nulles et si la calibration a ete faite?

		while True:


			self.lock.acquire()
			print("Start image analysis")

			# Ecrire le nom du path ou seront enregistrees les photos
			PathToFile = ""

			#os.system("streamer -s 1920x1080 -f jpeg -c /dev/video2 -b 16 -o ~/python_ws/Scripts_WorkShop_Avril/Test_Niveau//im_BU_level.jpeg")
			#os.system("streamer -s 1920x1080 -f jpeg -c /dev/video3 -b 16 -o ~/python_ws/Scripts_WorkShop_Avril/Test_Niveau/im_BR_level.jpeg")

			
			#camera3 = "\"Built-in iSight\""

			try : 
				os.system("imagesnap -d " + self.camera_AQ + " " + PathToFile + "im_AQ_level.jpeg")
			except Exception as e : 
				print(e)

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
