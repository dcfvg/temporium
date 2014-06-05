messages
=======

description                               |  patern               | message       | port |
----------------------------------------- | --------------------- | ------------- | ---- |
debut de séance                           | /seance_start         | 1             | 3333 | 
arret d'urgence                           | /seance_stop          | 1             | 3333 | 
fin de séance                             | /seance_end           | 1             | 3334 |
taux de formation de l'image              | /image_formation      | 0-255         | 3333 |
info :  premiere image capturée           | /first_photo          | 1             | 3334 |
debut de séance							  | /seance_start         | 1             | 3335 | 
path de la deniere image capturée         | /image_capture        | /public/0002.jpg        | 3333 |
afficher le negatif                       | /EF                   | expose        | 3333 |
afficher le flash                         | /EF                   | flash         | 3333 |
recharger le négatif                      | /EF                   | imgReload     | 3333 |   
arrêter le patch                          | /EF                   | kill          | 3333 |
remise à zéro du chrono                   | /EF                   | resetTime     | 3333 |



life_controller (Client : 3333)-> seance_controller (Server : 3333) : 

description                               |  patern               | message       | port |
----------------------------------------- | --------------------- | ------------- | ---- |
debut de séance                           | /seance_start         | 1             | 3333 | 
arret d'urgence                           | /seance_stop          | 1             | 3333 | 

seance_controller (Client : 3334) : -> life_controller : (Server : 3334) 

description                               |  patern               | message       | port |
----------------------------------------- | --------------------- | ------------- | ---- |
fin de séance                             | /seance_end           | 1             | 3334 |


seance_controller (Client : 3335) : -> client_formation_rate : (Server : 3335) 

description                               |  patern               | message       | port |
----------------------------------------- | --------------------- | ------------- | ---- |
debut de séance							  | /seance_start         | 1             | 3335 |
path de la deniere image capturée         | /image_capture        | /public/0002.jpg        | 3333 |


client_formation_rate (Client : 3333) : -> seance_controller : (Server : 3333)

description                               |  patern               | message       | port |
----------------------------------------- | --------------------- | ------------- | ---- |
taux de formation de l'image              | /image_formation      | 0-255         | 3333 |


Seance_controller interne : 
description                               |  patern               | message       | port |
----------------------------------------- | --------------------- | ------------- | ---- |
afficher le negatif                       | /EF                   | expose        | 3333 |
afficher le flash                         | /EF                   | flash         | 3333 |
recharger le négatif                      | /EF                   | imgReload     | 3333 |   
arrêter le patch                          | /EF                   | kill          | 3333 |
remise à zéro du chrono                   | /EF                   | resetTime     | 3333 |


Rq : 
Supprimé : 
description                               |  patern               | message       | port |
----------------------------------------- | --------------------- | ------------- | ---- |
info :  premiere image capturée           | /first_photo          | 1             | 3334 |
