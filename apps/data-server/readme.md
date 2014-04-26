# data-server

- pilotage à distance ( http://ni-c.github.io/heimcontrol.js/ ) 
- récolte des données du life controller
- timeline du film
- capatation microscopique
- projection vidéo du film ( http://www.matrox.com/graphics/fr/products/gxm/th2go/displayport/ ) 

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
- ffmpeg
- detox
- imagesnap
- vlc
- EOS Utility
- imagemagick
- 

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
