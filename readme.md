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
| connaitre le niveau               | moyenne| |

**bio-réacteurs**

| fonction                          | priorité | solution envisagée                                            |
| --------------------------------- | -------- |-------------------------------------------------------------- |
| agitater la culture               | critique | |
| aérer la culture                  | critique | |
| remettre à niveau avec du milieu  | critique | |
| connaitre la concentration        | moyenne  | |
| détecter une contamination        | faible   | |

**aquarium**

| fonction                          | priorité | solution envisagée                                            |
| --------------------------------- | -------- |-------------------------------------------------------------- |
| vider l'aquarium                  | critique | | 
| remplique l'aquarium              | critique | |
| ajuster la concentration          | critique | |
| maintenir le niveau               | critique | | 
| filtrer les impuretés             | critique | |

**recyclage**

| fonction                          | priorité | solution envisagée                                            |
| --------------------------------- | -------- |-------------------------------------------------------------- |
| stocker les cultures usagées      | critique | | 
| lyophiliser les cultures usagées  | faible   | | 


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
