### partition 
/public/score.csv`

[apps/interface/public/score.csv](https://github.com/dcfvg/temporium/blob/panorama/apps/interface/public/score.csv)

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

Le temps du vivant est figuré dans le film par un cache vert de 4 secondes.

### monitoring
`/monitor`


**fonctions** 
- redémarrage du Systeme
- donner l'état
- donner le niveau des différents organes 
- bloquer d'un biréacteur
- lire les logs

**interface ssh**
- en wifi sur place 
- en depuis l'extérieur par internet (bonus)
