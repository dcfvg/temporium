interface
=====

### installation
_depuis le terminal_
1. aller dans le dossier `cd ~/temporim/apps/interface/`
2. installer les modules nodejs `npm install`
3. création les dossiers pour les médias dans le dossier`interface/public/` 
	- `exposure`, l’emplacement des images capturées par l’appareil
	- `images`, l’emplacement pour l’image à exploser `nega.png` et du flash gris `flash.png`

### configuration du montage dynamique

- le fichier `[/public/score.csv](https://github.com/dcfvg/temporium/blob/panorama/apps/interface/public/score.csv)` permet de modifier les paramètres du montage dynamique.

| champ  | description |
| ------ | ----------- |
| id     | numéro d'évenement unique                    |
| title  | étiquette pour repérer les plans                      |
| mode   | in (avant contamination) / out (après contamination)
| at_min:at_sec | mode in : moment ou une interruption du plan est possible|
|        | mode out : moment avant lequel la lecture doit avoir reprise (mode out )|
| jump   | saut max en avant ou en arriere suivant le mode |
| life_speed | vitesse de défilement du timelapse — 1=vitesse normale / 8=ralenti 8 fois | 
| life_zoom  | grossisement de l'image 1-5 | 

> Le temps du vivant est figuré dans le film par un cache vert de 4 secondes.

### démarrage de l’application : 

_depuis le terminal_
1. aller dans le dossier `cd ~/temporim/apps/interface/`
2. démarrer le serveur node `node server.js`

_depuis le navigateur_
1. ouvrir `localhost:8080/player` pour afficher le film
2. ouvrir `localhost:8080/exposure` pour afficher l’image à exposer
3. **attendre** plusieurs minutes que le film ait le temps de se précharger

_depuis le vivant_
1. envoyer le message `seance_start`
2. envoyer le taux de formation en réponse à 

### utilisation du player
La console du navigateur permet de suivre l’état du player.

_raccourcits clavier_

- `m` montrer le film
- `l` montrer l’image live 
- `k` afficher le timecode courant dans la console
- `j` avancer le film de 10 s
- `h` avancer le film de 30 s

### utilisation de d'exposure

La page `/exposure` peut être déporté sur un autre poste en consultant `xxx.xxx.xxx.xxx:8080/exposure/` avec `xxx.xxx.xxx.xxx` l'ip du serveur sur le réseau local. .

### TODO

- interface de gestion du montage `/monitor`
- mise en place du lancement plein écran automatique
- mode debug qui affiche l'état du film
