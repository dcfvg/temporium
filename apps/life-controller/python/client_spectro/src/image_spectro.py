# Importation des bibliotheques
from PIL import Image 
import colorsys 
import time
import os
import threading
import numpy
from client_spectro import *
from thread_image_spectro import *
import subprocess

class image_spectro(threading.Thread):

	def __init__(self,un_client):


		threading.Thread.__init__(self)
		self.client = un_client

		"""Lock for start and stop image analysis"""
		
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
		self.stabilised_value_minimum = 5
		
		self.diff_max = 40
		
		"""Initialzation of values"""
		self.values = []
		self.values_mean = []
		self.number_value_mean = 10
		
		
		self._running_state = [threading.Lock(), False]
		
		self.read_all_config()
		
	
	
	def read_all_config(self):
		"""initialization of cropping values"""
		self.read_config_crop()
		self.read_config_calibration()
		self.read_config_camera()
		
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
					self.camera_SPECTRO = list[1].strip()
					
					
			file.close()
			
		except Exception as e : 
			print(str(e))
			print ("no file : config/config_camera.txt in the directory")
			
	# Read the values of TOP level and LOW level for each BU
	
	
	"""take a path of the image to crop, return the image cropped"""
	def image_cropping(self,image_to_treat,path_destination_name, coordinates_crop):

		

		an_image = image_to_treat.crop(coordinates_crop)

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
	
	
	def analyse_run(self):

		
		#print("Start concentration analysis")

		# Ecrire le nom du path ou seront enregistrees les photos
		PathToFile = "image/"

		#print ("capture")
		os.system("imagesnap -d " + self.camera_SPECTRO + " " + PathToFile + "im_spectro.jpeg")
		try : 
			succed = False
			while not succed : 
				#a = subprocess.Popen(["imagesnap -d " + self.camera_BR_BU + " " + PathToFile + "im_B_level.jpeg"])
				a = subprocess.Popen(["imagesnap", "-d", self.camera_SPECTRO ,PathToFile + "im_spectro.jpeg"])

				compt = 0
				while compt < 4 :
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
		#time.sleep(2)
		
		image_to_treat = Image.open(PathToFile + "im_spectro.jpeg")
		
		path_destination_name =PathToFile +"croppedImage_.jpeg"
		
		
		self.concentration_value = self.get_level(image_to_treat, path_destination_name, self.coordinates_crop)[0]
		if len(self.values) >0 :
			if abs( self.concentration_value - self.values[len(self.values)-1]) > self.diff_max :
				if not self.pb_previous : 
					self.concentration_value = self.values[len(self.values)-1]
				self.pb_previous = True
			
			else : 
				self.pb_previous = False
				 
		
		if len(self.values) < self.number_value_mean :
			self.values.append(self.concentration_value)
		else :
			new_value = (self.concentration_value + sum(self.values[(len(self.values)-self.number_value_mean)+1:]))/self.number_value_mean
			new_value = round(new_value,2)
			self.values.append(self.concentration_value)
			self.values_mean.append(new_value)
			self.concentration_value = new_value
		
		
		
		"""for testing if self.concentration_value is stabilised"""
		"""test on 10 previous values""" 
		stabilised = False
		if len(self.values_mean) > self.number_previous_values :
			"""rank of the last values"""
			rank = len(self.values_mean)-1
			stabilised_until = True
			for i in range(self.number_previous_values + 1) : 
				if abs(self.values_mean[rank-i]- self.values_mean[rank]) > self.stabilised_value_minimum : 
					stabilised_until = False 
			
			stabilised = stabilised_until
			
			
		
		print ("current value : " + str(self.concentration_value))
		"""in the shape : "AQ : 50,72"""
		"""pour tester""" 
		
		value = str(self.concentration_value)
		#value = value.replace("[","")
		#value = value.replace("]","")
		
		
		if stabilised :
			msg_to_send = "AQ :" +  value
			
			print(msg_to_send)
			
			self.client._send(msg_to_send)
			
			print("stabilised value :" + str(self.concentration_value))

		
		#print("End concentration analysis")
	"""to start analysis"""
	
	"""to start analysis"""
	def start_concentration(self):
		if not self.get_running_state() : 
			self.read_all_config()
			self.set_running_state(True)
			self.values = []
			self.values_mean = []
			self.pb_previous = False
			self.thread_image_spectro = thread_image_spectro(self)
			self.thread_image_spectro.start()
		else : 
			print ("already level analysis running" )
		
	"""to stop analysis"""
	def stop_concentration(self):
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
	