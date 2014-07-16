# Importation des bibliotheques	
from PIL import Image , ImageFilter
import colorsys 
import time
import os
import threading
from client_level import *
import random
import numpy
from thread_image_level import *
import subprocess



class image_level(threading.Thread):


	def __init__(self,un_client):
		# define parameters for the level_mesure function. To know their role, go and check the comments of that function.
		self.jump_pixel = dict()
		self.diff = dict()
		self.gaussian_radius = dict()
		self.nb_pixel_level_line = dict()
		
		self.config_detection_read_for = ["AQ"]

		threading.Thread.__init__(self)
		self.client = un_client


		"""if image is upside down"""
		self.image_upside_down = True
		
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

		"""time to wait for shooting photo"""
		self._time_wait_webcam = 8
		
		# Dictionnaries that gather of TOP and LOW levels for calibration
		self.calibration_values = {'AQ':{'HIGH':0,'LOW':0}}

		self._level= { 	"AQ" :  0}
		

		#print ("Cropping coordinates : " + str(self.calibration_values))

		self._running_state = [threading.Lock(), False]
		self.read_all_config()
		
		#print ("Cropping coordinates : " + str(self.calibration_values))
		
	
	def read_all_config (self):
		self.read_config_crop_AQ()
		self.read_calibration_AQ()
		self.read_config_camera()
		self.read_config_detection()
		
	def read_config_detection(self):
		print("read config detection")
		try : 
			file = open("config/config_detection_AQ.txt", "r")
			
	
			for ligne in file :
				"""Take out the end symbols (\n)"""
				ligne = ligne.strip()
				"""split on  ':' """
				list = ligne.split(":")	
				
				name_container = list[0].strip()
				for name in self.config_detection_read_for:
					if name_container == name :
						name_parameter = list[1].strip()
						value = int(list[2].strip())
						
						if name_parameter == "JUMP_PIXEL" : 
							self.jump_pixel[name_container] = value
						
						elif name_parameter == "DIFF" : 
							self.diff[name_container] = value
						
						elif name_parameter == "GAUSSIAN_RADIUS" :
							self.gaussian_radius[name_container] = value
							
						elif name_parameter == "NB_PIXEL_LEVEL_LINE" :
							self.nb_pixel_level_line[name_container] = value
			
			print (self.nb_pixel_level_line)
						
		except Exception as e : 
			print(str(e))
			
		

			#ce sont les limites le limage

			"""image full : the whole image, name : BR1 or BR2 ... crop :  where to crop = [x0, y0, x1, y1]"""
	

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
					self.camera_AQ = list[1].strip()
					
					
			file.close()
			
		except Exception as e : 
			print(str(e))
			
			
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
			
			


	# Read the coordinates for the image cropping of each BU 
	def read_calibration_AQ(self):
		print ("read calibration camera")
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

	def image_cropping(self,image_to_treat,path_destination_name, coordinates_crop):


		an_image = image_to_treat.crop(coordinates_crop)

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
		
		gaussian_radius = self.gaussian_radius[conteneur_name]
		diff = self.diff[conteneur_name]
		jump_pixel = self.jump_pixel[conteneur_name]
		nb_pixel_level_line = self.nb_pixel_level_line[conteneur_name]
			#print (conteneur_name + "gaussian_radius :  " + str(gaussian_radius))
			

		im = im.convert('L')
		im = im.filter(ImageFilter.GaussianBlur(radius = gaussian_radius))
		im = self.get_edges(im,jump_pixel,diff)

		level = []
		im = im.rotate(90)
		data = self.data_to_image(im)
		for j in range(width) :
			for i in range(height - nb_pixel_level_line) :
				if sum(data[j][i:i+nb_pixel_level_line]) == 0 :
					level.append(i+int(nb_pixel_level_line/2))

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
	
	def analyse_run(self):


		#ne rentrer dans le while que si les coordonnees ne sont pas toutes nulles et si la calibration a ete faite?

	
		print("Start image analysis")

		# Ecrire le nom du path ou seront enregistrees les photos
		PathToFile = ""

		#os.system("streamer -s 1920x1080 -f jpeg -c /dev/video2 -b 16 -o ~/python_ws/Scripts_WorkShop_Avril/Test_Niveau//im_BU_level.jpeg")
		#os.system("streamer -s 1920x1080 -f jpeg -c /dev/video3 -b 16 -o ~/python_ws/Scripts_WorkShop_Avril/Test_Niveau/im_BR_level.jpeg")

		
		#camera3 = "\"Built-in iSight\""

		try : 
			#os.system("imagesnap -d " + self.camera_AQ + " " + PathToFile + "im_AQ_level.jpeg")
			succed = False
			while not succed : 
				#a = subprocess.Popen(["imagesnap -d " + self.camera_BR_BU + " " + PathToFile + "im_B_level.jpeg"])
				a = subprocess.Popen(["imagesnap", "-d", self.camera_BR_BU ,PathToFile + "im_AQ_level.jpeg"])

				compt = 0
				while compt < self._time_wait_webcam :
					time.sleep(1)
					compt = compt +1
					#print ("wait" + str(compt))
				if a.poll() == None :
					print ("camera lost, new try") 
					a.kill()
					time.sleep(1)
				else : 
					succed = True
					print ("Image taken")
		except Exception as e : 
			print(e)

		#time.sleep(1)


		#Path jusqu'a l'image a cropper 
		image_AQ = Image.open(PathToFile + "im_AQ_level.jpeg")
		
		if self.image_upside_down : 
			image_AQ = image_AQ.rotate(180)

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

		print("End image analysis")

	"""to start analysis"""
	def start_level(self):
		if not self.get_running_state() : 
			self.read_all_config()
			self.set_running_state(True)
			self.thread_image_level = thread_image_level(self)
			self.thread_image_level.start()
		else : 
			print ("already level analysis running" )
		
	"""to stop analysis"""
	def stop_level(self):
		self.set_running_state(False)
	"""do not use this function"""
	def get_running_state(self):
		self._running_state[0].acquire()
		state = self._running_state[1]
		self._running_state[0].release()
		return state
		
	def set_running_state(self, state):
		self._running_state[0].acquire()
		self._running_state[1]= state
		self._running_state[0].release()