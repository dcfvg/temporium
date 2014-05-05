messages
=======

description                               |  patern               | message       | port |
----------------------------------------- | --------------------- | ------------- | ---- |
debut de séance                           | /session              | begin         | 4141 | 
fin de séance                             | /session              | end           | 4141 |
afficher le negatif                       | /exposeFlashCommander | EF_expose     | 4242 |
afficher le flash                         | /exposeFlashCommander | EF_flash      | 4242 |
recharger le négatif                      | /exposeFlashCommander | EF_imgReload  | 4242 |   
arrêter le patch                          | /exposeFlashCommander | EF_kill       | 4242 |
remise à zéro du chrono                   | /exposeFlashCommander | EF_resetTime  | 4242 |
taux de formation de l'image              | /image_formation      | 0-255         | 4242 |

