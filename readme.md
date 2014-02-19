# temporium

## about
**Le Temporium** est une structure en verre mêlant des systèmes biologiques, mécaniques et  informatiques. Il se compose de **trois "étages-organes"** qui s'activent successivement et participent à l'écriture narrative du flm.

## installation
- les médias sont déposés dans un dossier `assets` (ignoré) à créer à la racine du répertoire.

````
assets
  - archive ( images exposés ) 
  - captation ( image de l'exposition ) 
  - waitinglist ( images en attente )
````

## dépendances

- processing-java
- sikuli
- ffmpeg
- detox
- imagesnap
- vlc
- EOS Utility
- imagemagick

___

### tâches

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
| lancer l'exposition               | critique | |
| capturer la formation (macro)     | critique | |
| compiler le timelaps              | critique | |
| live de la formation (micro)      | critique | |
| détecter la formation de l'image  | haute    | |
| récolter des données              | faible   | |
| controller à distance             | haute    | |
| vidéosurveiller à distance        | faible   | |
| détecter une contamination        | moyenne  | | 

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
