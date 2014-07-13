from PIL import Image, ImageFilter
import colorsys
import numpy




class image_level():


	def __init__(self,un_window):
		# define parameters for the level_mesure function. To know their role, go and check the comments of that function.
		self.jump_pixel = dict()
		self.diff = dict()
		self.gaussian_radius = dict()
		self.nb_pixel_level_line = dict()

		"""for pao method"""
		self.method_pao = True

		self.window = un_window
		
		self.config_detection_read_for = ["BR1", "BR2", "BR3"]
		
		self.read_config_detection()
	
		

#ce sont les limites le limage

	"""image full : the whole image, name : BR1 or BR2 ... crop :  where to crop = [x0, y0, x1, y1]"""
	def read_config_detection(self):
		print("read")
		try : 
			file = open("config/config_detection_BU.txt", "r")
			
	
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
					
						
		except Exception as e : 
			print(str(e))
			print ("no file : config_crop_BU.txt in the directory")
		

			#ce sont les limites le limage

			"""image full : the whole image, name : BR1 or BR2 ... crop :  where to crop = [x0, y0, x1, y1]"""
	
	
	def get_level(self,image_full_name, name_container,  crop):
		
		image_full = Image.open(image_full_name)
		self.image_cropping(image_full, name_container,crop[0], crop[1], crop[2], crop[3] )
		
		return self.level_mesure(name_container+".jpg", name_container)
		
		
	def image_cropping(self, image_a_traiter,outfile,a,b,c,d):

		uneImage = image_a_traiter.crop((a,b,c,d))
		
		uneImage.save(outfile+".jpg","jpeg")


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
		image.show()
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


	def level_mesure(self,image_a_tester, name_container):

		#Detecte le niveau de rouge d'une image pour sortir le niveau de liquide
		im = Image.open(image_a_tester)  #Import the image 
		width,height = im.size

		if self.method_pao : 
			
			
			gaussian_radius = self.gaussian_radius[name_container]
			diff = self.diff[name_container]
			jump_pixel = self.jump_pixel[name_container]
			nb_pixel_level_line = self.nb_pixel_level_line[name_container]
			#print (name_container + "gaussian_radius :  " + str(gaussian_radius))
			
			im = im.convert('L')
			im  = im.filter(ImageFilter.GaussianBlur(radius = gaussian_radius ))
			im = self.get_edges(im,jump_pixel,diff)

			level = []
			im = im.rotate(90)
			data = self.data_to_image(im)
			for j in range(width) :
				for i in range(height - nb_pixel_level_line) :
					if sum(data[j][i:i+nb_pixel_level_line]) == 0 :
						level.append(i+int(nb_pixel_level_line/2))

			if len(level) != 0 :


				#pourcentage_niveau = int(100*random.random())
				return float(numpy.mean(level))
			else:
	 
				print("no edges have been detected")
				return 'null'
		
		else : 
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

			for i in range(0,height*width,pas):
				u = colorsys.rgb_to_hls(rouge[i]/255.0,vert[i]/255.0,bleu[i]/255.0)
				

				
				if ((u[1]< 0.7) & (u[1]>0.1) & (u[0]>0.9 or u[0]<0.1)& (u[2]>0.025)):   #Calibrates the color red selected
					color.append([i%width,(i-i%width)/width,u[0]])
					somme_pixels = somme_pixels + 1	
					
				
				if ( ((i)%width) > (((i+pas))%width) ):
					vecteur_pixels.append(somme_pixels)
					somme_pixels=0
				

			#print  "\n"+ "niveau de remplissage :" + str(float(pourcentage_niveau)) + "%" +"\n"
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

			

			if somme_longueur != 0 :
				le_centre = le_centre/(float(somme_longueur))
				

				"""return the center : where the level has been detected"""
				return le_centre

			else:

				print ("no red has been detected")
				return ("null")
