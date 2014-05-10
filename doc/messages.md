messages
=======


osc-web : ecoute 3333 emet sur 3334


description                               |  patern               | message       | port |
----------------------------------------- | --------------------- | ------------- | ---- |
debut de séance                           | /seance               | begin         | 3333 | 
fin de séance                             | /seance               | end           | 3334 |
taux de formation de l'image              | /image_formation      | 0-255         | 3333 |
afficher le negatif                       | /exposeFlashCommander | EF_expose     | 3333 |
afficher le flash                         | /exposeFlashCommander | EF_flash      | 3333 |
recharger le négatif                      | /exposeFlashCommander | EF_imgReload  | 3333 |   
arrêter le patch                          | /exposeFlashCommander | EF_kill       | 3333 |
remise à zéro du chrono                   | /exposeFlashCommander | EF_resetTime  | 3333 |
