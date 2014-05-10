messages
=======


osc-web : ecoute 3333 emet sur 3334
http://automata.cc/osc-web

description                               |  patern               | message       | port |
----------------------------------------- | --------------------- | ------------- | ---- |
debut de séance                           | /seance_start         | 1             | 3333 | 
fin de séance                             | /seance_end           | 1             | 3334 |
taux de formation de l'image              | /image_formation      | 0-255         | 3333 |
id de la deniere image capturée           | /image_captureId      | 0-5000        | 3333 |
afficher le negatif                       | /EF                   | EF_expose     | 3333 |
afficher le flash                         | /EF                   | flash         | 3333 |
recharger le négatif                      | /EF                   | imgReload     | 3333 |   
arrêter le patch                          | /EF                   | kill          | 3333 |
remise à zéro du chrono                   | /EF                   | resetTime     | 3333 |
