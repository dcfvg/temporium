montage dynamique 
====

- projeter le film
- varier la durée des plans
- taux de formation de l’image de 0 à 255 donnée en OSC

## fonctionnement du player


| event                           | action du player                                                  |
| -----                           | ---                                                               |
| signal osc `session_start`      | **diffuser** le film                                                  |
| arrivée à `mark_live`           | **charger** et **diffuser** la `séquence générée` à la place du `film`    |
| fin de `séquence générée`       | **reprendre** la lecture du `film`                                    |
| arrivée à une `mark_at`         | **avancer** à l’une des 3 `mark_jump` en fonction de `taux_formation`  |
| fin du film                     | **remettre à zéro** le player et **envoyer** le signal osc `session_end`  |

**définition des objets**

| terme                       | définition |
| ---                         | ---- |
| `séquence générée`          | séquence JPG ou une vidéo générée par l'[outil de capture](https://github.com/dcfvg/temporium/tree/panorama/apps/capture) |
| `film`                      | version longue du film accompagné d’une bande-son (surround / 5.1) |
| `mark_????`                 | timecode ou numéro d'image connu à l'avance |
| `taux_formation`            | avancement (de 0 à 255) de la formation de l'image vivante communiquée par OSC |
| `session_start`             | signal de début de séance |
| `session_end`               | signal de fin de séance |

**Exemple de marqueurs**



| at	          | jumps         | `taux_formation`   |
| ------------- | ------------- | ----- |
| 00:10:20      | 00:10:20		  | 80  	|
| 			        | 00:10:40		  | 100 	|
| 			        | 00:12:00		  | 120 	|
| 00:18:20      | 00:18:00		  | 150 	|
| 			        | 00:18:40		  | 200 	|
| 			        | 00:20:00	  	| 250 	|

- `at` l’instant où il est possible de sauter
- `jumps` les moments vers lesquels on peut sauter
- `val` le seuil qui permet de choisir le saut en fonction du `taux_formation`
