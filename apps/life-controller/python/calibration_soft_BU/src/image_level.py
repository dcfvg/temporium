from PIL import Image 
import colorsys




class image_level():


	def __init__(self,un_window):

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

