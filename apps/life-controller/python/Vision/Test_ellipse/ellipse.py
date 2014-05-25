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




a=0

"""while  a<300:
	

	os.system("streamer -s 1920x1080 -f jpeg -c /dev/video2 -b 16 -o /home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Test_ellipse/ellipse" + str(a) + ".jpeg")

	time.sleep(15)

	a+=1



print 2/a
	
une photo toutes les 30 secondes : """





def level_mesure(image_a_tester):

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
		#niveau_moyenne = 0
		#nb_pixels = 0
		#ordonnee = 0

		for i in xrange(0,height*width,pas):
			u = colorsys.rgb_to_hls(rouge[i]/255.0,vert[i]/255.0,bleu[i]/255.0)
			

			
			if ((u[1]< 0.5) & (u[1]>0.1) & (u[0]>0.9 or u[0]<0.1)& (u[2]>0.1)):   #Calibrates the color red selected
				color.append([i%width,(i-i%width)/width,u[0]])
				somme_pixels = somme_pixels + 1    
				#nb_pixels += 1
				#ordonnee += (i-i%width)/width

				
			
			if ( ((i)%width) > (((i+pas))%width) ):
				vecteur_pixels.append(somme_pixels)
				somme_pixels=0


			
		position_max = vecteur_pixels.index(max(vecteur_pixels))

		pourcentage_niveau = (float(height)-float(position_max))/float(height)
		pourcentage_niveau = round(pourcentage_niveau,4)

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

		for i in xrange(len(vecteur_pixels2)):
			if (i+1 == len(vecteur_pixels2)):
				if (vecteur_pixels2[i] != 0):
					vec_pics.append([nb_pics,longueur_pic])

			else:
				if (vecteur_pixels2[i]== 0):
					if (vecteur_pixels2[i+1] != 0):
						nb_pics +=1

				if (vecteur_pixels2[i] != 0):

					if(vecteur_pixels2[i+1]!=0):
						longueur_pic +=1

					if(vecteur_pixels2[i+1] == 0):
						vec_pics.append([nb_pics,longueur_pic])
						longueur_pic = 0








		#niveau_moyenne = float(ordonnee)/float(nb_pixels)

		#return pourcentage_niveau
		#print pourcentage_niveau
		return [pourcentage_niveau,vecteur_pixels2,vec_pics] 

def image_cropping(image_a_traiter,outfile,a,b,c,d):


	im = Image.open(image_a_traiter)

	uneImage = im.crop((a,b,c,d))

	uneImage.save(outfile,"jpeg")


# image de cote : 864,400,940,800


# image au centre : 1000,400,1065,800


vec_centre = []
vec_cote =[]
vec_total = []



"""for i in range(3,60):

	uneImage = "/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Test_ellipse/ellipse" + str(i) + ".jpeg"

	outfile = "/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Test_ellipse/Cote/croppedImage_" + str(i) + ".jpeg"

	image_cropping(uneImage,outfile,864,400,940,750)
	
	vec_cote.append(level_mesure(outfile)[0])

	fig2 = plt.figure()
	plt.grid(True)
	plt.plot(level_mesure(outfile)[1])
	plt.show()


"""

"""for i in range(3,60):

	uneImage = "/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Test_ellipse/ellipse" + str(i) + ".jpeg"

	outfile = "/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Test_ellipse/Centre/croppedImage_" + str(i) + ".jpeg"

	image_cropping(uneImage,outfile,1000,400,1065,800)

	vec_centre.append(level_mesure(outfile)[0])
	fig2 = plt.figure()
				plt.grid(True)
				plt.plot(level_mesure(outfile)[1])
				plt.show()"""

for i in range(3,5):

	uneImage = "/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Test_ellipse/ellipse" + str(i) + ".jpeg"

	outfile = "/home/edgar/python_ws/Scripts_WorkShop_Avril/Test_Niveau/Test_ellipse/Total/croppedImage_" + str(i) + ".jpeg"

	image_cropping(uneImage,outfile,960,400,1090,800)

	vec_total.append(level_mesure(outfile)[0])
	print(level_mesure(outfile)[2])
	fig2 = plt.figure()
	plt.grid(True)
	plt.plot(level_mesure(outfile)[1])
	plt.show()






"""print vec_cote
print vec_centre"""


#print(level_mesure("ellipse0.jpeg"))

"""vec = numpy.array(vec_centre)
pylab.plot(vec)
#pylab.legend('b')
pylab.xlabel('Numero de la photo')
pylab.ylabel('pourcentage de remplissage')
pylab.grid(True)
pylab.title('Pourcentage de remplissage en regardant le cote du BU')
pylab.show()

vec = numpy.array(vec_cote)
plt.plot(vec)
#pylab.legend('b')
plt.xlabel('Numero de la photo')
plt.ylabel('pourcentage de remplissage')
plt.grid(True)
plt.title('Pourcentage de remplissage en regardant le cote du BU')
plt.show()

vec = numpy.array(vec_total)
plt.plot(vec)
#pylab.legend('b')
plt.xlabel('Numero de la photo')
plt.ylabel('pourcentage de remplissage')
plt.grid(True)
plt.title('Pourcentage de remplissage en regardant le cote du BU')
plt.show()




fig = plt.figure()
plt.grid(True)
plt.plot(vec_cote, 'b-')

plt.plot(vec_centre, 'g-')

plt.plot(vec_total, 'r-')

plt.show()"""

