# temporium
![](https://kkbb-production.s3.amazonaws.com/uploads/project_image/image/66765/renduallum02.jpg)

> **Le Temporium** est une structure en verre mêlant des systèmes biologiques, mécaniques et  informatiques. Il se compose de **trois "étages-organes"** qui s'activent successivement et participent à l'écriture narrative du flm.




### tâches

**structure**

| fonction                          | priorité | solution envisagée                                            |
| --------------------------------- | -------- |-------------------------------------------------------------- |
| maintenir la température          | critique | chauffage d'appoint + circulation d'air                       |

**milieux**

| fonction                          | priorité | solution envisagée                                            |
| --------------------------------- | -------- |-------------------------------------------------------------- |
| connaitre le niveau               | moyenne  | electrode ( juste max ) — flotteur — imagerie                 |

**bio-réacteurs**

| fonction                          | priorité | solution envisagée                                            |
| --------------------------------- | -------- |-------------------------------------------------------------- |
| agitter la culture                | critique | bareau magnétique, microbulles ( par dessous )                |
| aérer la culture                  | critique | pompe à air                                                   |
| maintenir le niveau (+ milieu)    | critique | pompe + electrode — flotteur — imagerie                       |
| connaitre la concentration        | moyenne  | webcam                                                        |
| détecter une contamination        | faible   | webcam, microsopie                                            |

**aquarium**

| fonction                          | priorité | solution envisagée                                            |
| --------------------------------- | -------- |-------------------------------------------------------------- |
| vider l'aquarium                  | critique | pompe                                                         |
| remplir l'aquarium                | critique | pompe                                                         |
| ajuster la concentration          | critique | pompe + webcam + analyse d'image                              |
| maintenir le niveau               | critique | pompe + electrode — flotteur — imagerie                       | 
| filtrer les impuretés             | critique | pompe/filtre ( trop puissante pour l'instant )                |
| nettoyer la vitre                 | critique | magnet + rails — bras en croix                                | 

**recyclage**

| fonction                          | priorité | solution envisagée                                            |
| --------------------------------- | -------- |-------------------------------------------------------------- |
| stocker les cultures usagées      | critique | bidon                                                         |
| lyophiliser les cultures usagées  | faible   | bac à galçons + lyophilisateur                                |


**imagerie & données**

| fonction                          | priorité | solution envisagée                                            |
| --------------------------------- | -------- |-------------------------------------------------------------- |
| lancer l'exposition               | critique | [gphoto](http://www.gphoto.org/) [canon-remote](http://pythonhosted.org/canon-remote/index.html)|
| capturer la formation (macro)     | critique | boitier canon + pilotage
| compiler le timelaps              | critique | [ffmpeg](http://www.ffmpeg.org)
| live de la formation (micro)      | critique | ?? |
| détecter la formation de l'image  | haute    | webcam + |
| récolter des données              | faible   | ?? |
| controller à distance             | haute    | [heimcontrol.js](http://ni-c.github.io/heimcontrol.js)|
| vidéosurveiller à distance        | faible   | webcam |

**montage dynamique & conduite**

| fonction                           | priorité | solution envisagée                                            |
| ---------------------------------- | -------- |-------------------------------------------------------------- |
| actionner le mode entretien        | critique | |
| lancer une séance automatiquement  | critique | | 
| afficher les prochainnes séances   | haute    | |
| insérer de plans dans le film      | critique | |
| varier la durée de plans           | haute    | |
| produire le son en direct          | faible   | |
| enregistrer la séance              | haute    | |
