from PIL import Image, ImageFilter
import colorsys
import numpy




class image_level():


	def __init__(self,un_window):
		# define parameters for the level_mesure function. To know their role, go and check the comments of that function.
		self.k = 1
		self.diff = 5
		self.gaussian_radius = 2
		self.nb_pixel_level_line = 5

		self.window = un_window


	#ce sont les limites le limage

	"""image full : the whole image, name : BR1 or BR2 ... crop :  where to crop = [x0, y0, x1, y1]"""

	def get_level(self,image_full, name,  crop):
		self.image_cropping(image_full, name,crop[0], crop[1], crop[2], crop[3] )
		return self.level_mesure(name+".jpg")

	
	def image_cropping(self, image_a_traiter,outfile,a,b,c,d):
		im = Image.open(image_a_traiter)

		uneImage = im.crop((a,b,c,d))

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

	def level_mesure(self,image_a_tester):
		im = Image.open(image_a_tester)  #Import the image 
		width,height = im.size

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
			#pourcentage_niveau = (1-float(numpy.mean(level))/float(calibrated_height))*100
			#pourcentage_niveau = round(pourcentage_niveau,4)
 
			#pourcentage_niveau = int(100*random.random())
			return float(numpy.mean(level))
		else:
 
			print("no edges have been detected")
			return 'null'
