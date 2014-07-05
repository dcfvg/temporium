# Importation des bibliotheques
from PIL import Image 
import colorsys 
import time
import os
import threading
import numpy
from client_spectro import *

class image_spectro(threading.Thread):

	def __init__(self,un_client):


		threading.Thread.__init__(self)
		self.client = un_client

		"""Lock for start and stop image analysis"""
		
		self.lock = threading.Lock()
		self.lock.acquire()
		
		self.concentration_value = None
		
		"""coord of cropping : tulpe"""
		self.coordinates_crop = [0,0,0,0]
		"""maximun and minimum for concentration, to have a rate in %"""
		self.high_C = 0
		self.low_C = 0
		
		"""camera_SPECTRO is used when only one camera"""
		""" Camera names (use imagesnap -l to identify)"""
		self.camera_SPECTRO =""
		
		"""stabilised parameter""" 
		"""number of previous values for stabilisation"""
		self.number_previous_values = 10
		"""value of the maximum difference of the values to be considered as stabilised"""
		self.stabilised_value_minimum = 3
		
		
		"""initialization of cropping values"""
		self.read_config_crop()
		self.read_config_calibration()
		self.read_config_camera()

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
				
				if list[0].strip() == "SPECTRO" :
					self.camera_SPECTRO = "\"" + list[1].strip() +"\""
					
					
			file.close()
			
		except Exception as e : 
			print(str(e))
			print ("no file : config/config_camera.txt in the directory")
			
	# Read the values of TOP level and LOW level for each BU
	
	
	"""take a path of the image to crop, return the image cropped"""
	def image_cropping(self,path_image_to_treat,path_destination_name, coordinates_crop):

		im = Image.open(path_image_to_treat)

		an_image = im.crop(coordinates_crop)

		an_image.save(path_destination_name,"jpeg")
		
		return an_image


	def absorption(self,image_to_treat):
		
		#im = Image.open(image_to_treat)
		"traite une image en niveau de gris"
		"appeler une commande sur le terminal"
		
		im = image_to_treat
		
		data=list(im.getdata())
		mean = round(numpy.mean(data),1)
		
		"""result in %, after the calibration"""
		result = [100 - int(((mean-self.high_C)/(self.low_C-self.high_C))*100), int(mean)]

		"""answer an [%, real value] array"""
		return result
	
	def get_level(self,path_image_to_treat, path_destination_name, coordinates_crop):
		
		"""crop the image"""
		im_cropped = self.image_cropping(path_image_to_treat, path_destination_name, coordinates_crop)
		
		"""result : [%,real,value]"""
		result = self.absorption(im_cropped)
		
		return result
	
	def run(self):

		while True:
			self.lock.acquire()
			#print("Start concentration analysis")

			# Ecrire le nom du path ou seront enregistrees les photos
			PathToFile = "image/"

			
			stabilised = False
			values = []
			while not stabilised and not self._stop : 
				#print ("capture")
				os.system("imagesnap -d " + self.camera_SPECTRO + " " + PathToFile + "im_spectro.jpeg")
				time.sleep(2)
				
				path_image_to_treat = PathToFile + "im_spectro.jpeg"
				path_destination_name =PathToFile +"croppedImage_.jpeg"
				
				
				self.concentration_value = self.get_level(path_image_to_treat, path_destination_name, self.coordinates_crop)[0]
				
				values.append(self.concentration_value)
				
				"""for testing if self.concentration_value is stailised"""
				"""test on 10 previous values""" 
				if len(values) > self.number_previous_values :
					"""rank of the last values"""
					rank = len(values)-1
					stabilised_until = True
					for i in range(self.number_previous_values + 1) : 
						if abs(values[rank-i]- values[rank]) > self.stabilised_value_minimum : 
							stabilised_until = False 
					
					stabilised = stabilised_until
					
					
				
				print ("current value : " + str(self.concentration_value))
				
			print ("stabilised value " + str(self.concentration_value))
			"""in the shape : "AQ : 50,72"""
			value = str(self.concentration_value)
			#value = value.replace("[","")
			#value = value.replace("]","")
			
			msg_to_send = "AQ :" +  value
			
			print(msg_to_send)
			

			self.client._send(msg_to_send)

			self.lock.release()
			
			if self._stop : 
				self._stop_concentration()
			
			#print("End concentration analysis")
	"""to start analysis"""
	def start_concentration(self):
		self._stop = False
		self.lock.release()
	"""to stop analysis"""
	def stop_concentration(self):
		self._stop = True
	"""do not use this function"""
	def _stop_concentration(self):
		self.lock.acquire()
		
	def read_config_crop(self):
		print("read crop values")
		try : 
			file = open("config/config_crop_SPECTRO.txt", "r")
			
	
			for ligne in file :
				"""Take out the end symbols (\n)"""
				ligne = ligne.strip()
				"""split on  ':' """
				list = ligne.split(":")	
				
				if list[0].strip() == "SPECTRO" :
					coord = list[1].split(",")
					"""covert in int """
					self.coordinates_crop[0] = int(coord[0].strip())
					self.coordinates_crop[1] = int(coord[1].strip())
					self.coordinates_crop[2] = int(coord[2].strip())
					self.coordinates_crop[3] = int(coord[3].strip())
			
			file.close()
			
		except Exception as e : 
			print(str(e))
			print ("no file : config/config_crop_SPECTRO.txt in the directory")
			
	
	def read_config_calibration(self):
		print("read calibration values")
		try : 
			file = open("config/config_calibration_SPECTRO_HIGH.txt", "r")
			
	
			for ligne in file :
				"""Take out the end symbols (\n)"""
				ligne = ligne.strip()
				"""split on  ':' """
				list = ligne.split(":")	
				
				if list[0].strip() == "SPECTRO" :
					if list[1].strip() == "HIGH" :
						self.high_C = int(list[2].strip())
					else : 
						print("PB WITH THE FILE")
			
			file.close()
			print("C max : " + str(self.high_C))	
				
		except Exception as e : 
			print(str(e))
			print ("no file : config/config_calibration_SPECTRO_HIGH.txt in the directory")
		
		try : 
			file = open("config/config_calibration_SPECTRO_LOW.txt", "r")
			
	
			for ligne in file :
				"""Take out the end symbols (\n)"""
				ligne = ligne.strip()
				"""split on  ':' """
				list = ligne.split(":")	
				
				if list[0].strip() == "SPECTRO" :
					if list[1].strip() == "LOW" :
						self.low_C = int(list[2].strip())
					else : 
						print("PB WITH THE FILE")
			
			file.close()
			print("C min : " + str(self.low_C))	
				
		except Exception as e : 
			print(str(e))
			print ("no file : config/config_calibration_SPECTRO_LOW.txt")
		