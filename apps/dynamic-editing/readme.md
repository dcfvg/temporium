# montage dynamique 

- projeter le film
- varier la durée des plans
- taux de formation de l'image de 0 à 255 donnée en OSC

**table de décision**

- `at` l'instant ou il est possible de sauter
- `jumps` les moments vers lequels on peu sauter
- `val` le seuil qui permet de choisir le saut en fonction du taux de formation (0-255)

| at	          | jumps         | val   |
| ------------- | ------------- | ----- |
| 00:10:20      | 00:10:20		  | 80  	|
| 			        | 00:10:40		  | 100 	|
| 			        | 00:12:00		  | 120 	|
| 00:18:20      | 00:18:00		  | 150 	|
| 			        | 00:18:40		  | 200 	|
| 			        | 00:20:00	  	| 250 	|
