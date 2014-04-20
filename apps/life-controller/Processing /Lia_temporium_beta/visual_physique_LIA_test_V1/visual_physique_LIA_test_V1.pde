
	import processing.serial.*;
	import cc.arduino.*;

	float share_visual_x;
	float share_visual_y;  

	container M1;
	container M2;

	container BR1;
	container BR2;
	container BR3;

	container BU1;
	container BU2;
	container BU3;

	container AQ;

	container S;

	container[] les_container;

	  //Arduino : 

	Arduino arduino;

	//Input et Output : 
	BufferedReader reader; 
	PrintWriter writer_start;
	PrintWriter writer_end;
	

	//!\\Début du code concernant les cycles BR/BU

	int step ;
	boolean occupied ; 
	boolean BR1_filled_M1 ; 
	boolean BU1_filled_BR1 ;
	boolean BU1_filled_M2 ;
	boolean BU1_empty; 
	int P_BR1_BU1 ;
	int P_M1_BR1 ;
	int P_BU1_AQ ;
	int P_M2_BU1 ;

	boolean[] AQ_filled_BU1;
	
	int number_time_BU1_used;
	int number_time_BU2_used;
	int number_time_BU3_used;


	boolean start_step_0 ;
	boolean start_step_1 ;
	boolean start_step_2 ;
	boolean start_step_3 ;
	boolean start_step_4 ;
	boolean start_step_5 ;
	boolean start_step_6 ;
	boolean start_step_7 ;



	//Position des elements 
	float[] position_BR1;
	float[] position_BR2;
	float[] position_BR3;

	float[] position_BU1;
	float[] position_BU2;
	float[] position_BU3;

	float[] position_M1; 
	float[] position_M2;

	float[] position_AQ;
	float[] position_S;

	//Dimension des éléments: 

	float[] dimension_M; 
	float[] dimension_BR;
	float[] dimension_BU;
	float[] dimension_AQ;
	float[] dimension_S;

	//Volume des container 
	float volume_M;
	float volume_BR;
	float volume_BU;
	float volume_AQ;
	float volume_S;

	//Pompes
	pompe[] les_pompes;

	float debit_pompe;

	//String[] digit_pompe; //Nom des pompes dans l'ordre des pin digital
	String[] numero_cont;//numero des cont 

	//time entre deux rafraichissement;
	float time_rate; 
	int currenttime;
	int oldtime;

	float time_second ; 
	float time_minute ;
	float time_hour ; 
	float time_hour_C1 ; 
	float time_hour_C2; 
	float time_hour_C3 ; 


	int time_start_year ;
	int time_start_month ; 
	int time_start_day ;
	int time_start_hour ;
	int time_start_minute ; 
	int time_start_second  ;

	//Etat des cycles : 1 = wait / 2 = use / = 3 empty 
	int state_cycle_C1;
	int state_cycle_C2;
	int state_cycle_C3;

	int compteur_log;
	int comteur_use_BU1;
	int comteur_use_BU2;
	int comteur_use_BU3;

	//Electrodes : 
	float[] EL_M;
	float[] EL_BR;	
	float[] EL_BU;
	float[] EL_AQ;
	float[] EL_S;

	//Buffer used :
	String BU_USED; 



	public void setup(){
		size(900,800);
		background(150);

	    ////Pour choisir le bon port ou l'arduino est branché 
		println(Arduino.list());

		arduino = new Arduino(this, Arduino.list()[2], 57600);

		
		//on initialise la partie visuelle 
		share_visual_x = 0.7;
		share_visual_y = 1; 
		
		//Electrodes : Nombre et place des electrodes dans chaque type de container 

		EL_M = new float[1];
		EL_M[0] = 0.05 ; //EL a 5% du fond. 
		
		EL_BR = new float[3];
		EL_BR[0] = 0.01 ; //1%
		EL_BR[1] = 0.33 ; //33%
		EL_BR[2] = 1 ; //100%
		
		//Provisoire
		EL_BU = new float[4];
		EL_BU[0] = 0.01 ; //1%
		EL_BU[1] = 0.33 ; //33%
		EL_BU[2] = 0.66 ; //66%
		EL_BU[3] = 1 ; //100%
		
		EL_AQ = new float[3];
		EL_AQ[0] = 0.01 ; //1%
		EL_AQ[1] = 0.9 ; //0.6875 ; //68,75% car, aq 8L , donc vidage de 2,5L a chaque fois.  
		EL_AQ[2] = 1 ; //100%
		
		EL_S = new float[1];
		EL_S[0] = 0.9 ; //90%
		
		
		//On initilise les positions (de 0 à 1, en pourcentage de la taille de la fenetre): 0.16 de hauteru pour les containers // 0.05 pour pompes-tuyaux

		position_M1 = new float[2];
		position_M1[0] = 0;
		position_M1[1] = 0;

		position_M2 = new float[2];
		position_M2[0] = (float) 0.7;
		position_M2[1] = (float) 0;

		position_BR1 = new float[2];
		position_BR1[0] =(float)  0;
		position_BR1[1] =(float)  (0.16+0.05);

		position_BR2 = new float[2];
		position_BR2[0] =(float)  0.2;
		position_BR2[1] = (float) (0.16+0.05);

		position_BR3 = new float[2];
		position_BR3[0] =(float)  0.4;
		position_BR3[1] = (float) (0.16+0.05);

		position_BU1 = new float[2];
		position_BU1[0] =(float)  0;
		position_BU1[1] =(float)  (2*(0.16+0.05));

		position_BU2 = new float[2];
		position_BU2[0] =(float)  0.2;
		position_BU2[1] = (float) (2*(0.16+0.05));

		position_BU3 = new float[2];
		position_BU3[0] =(float)  0.4;
		position_BU3[1] = (float) (2*(0.16+0.05));

		position_AQ = new float[2];
		position_AQ[0] = (float) 0.2;
		position_AQ[1] = (float) (3*(0.16+0.05));


		position_S = new float [2];
		position_S[0] = (float) 0.2;
		position_S[1] =(float)  (4*(0.16+0.05));

		//On initialise les proportions (de 0 à 1 en pourcentage de la fenetre);

		dimension_M = new float[2];
		dimension_M[0] = (float) 0.3;
		dimension_M[1] = (float) 0.16;

		dimension_BR = new float[2];
		dimension_BR[0] =(float)  0.1;
		dimension_BR[1] =(float)  0.16;

		dimension_BU = new float[2];
		dimension_BU[0] =(float)  0.1;
		dimension_BU[1] =(float)  0.16;

		dimension_AQ = new float[2];
		dimension_AQ[0] = (float) 0.5;
		dimension_AQ[1] = (float) 0.16;

		dimension_S = new float [2];
		dimension_S[0] = (float) 0.2;
		dimension_S[1] =(float)  0.16; 
		

		//PARIE PARAMETRABLE\\
		
		///////////////\\\\\\\\\\\\\\\
		//Volume réel des trucs litre\\
		//\\\\\\\\\\\\\\\////////////////

		volume_M = (float) 8 ; 
		volume_BR =(float) 1.8 ;
		volume_BU =(float) 1.8  ;
		volume_AQ =(float) 40 ;
		volume_S = (float) 1 ;
		
		//////////\\\\\\\\\
		//Debit des pompes \\
		//\\\\\\\\\\\//////////
		debit_pompe = (float) 0.05;//en L/min

		///////////////\\\\\\\\\\\\\\\
		//\\\\\\\\\\\\\\\///////////////


		compteur_log=0;
		comteur_use_BU1 = 0;
		comteur_use_BU2 = 0;
		comteur_use_BU3 = 0;


		//Instanciation des differents objets, avec bonne dimension :  
		//Container(position, numero, type, nom)
		les_container = new container[10];
		//les milieux
		M1 = new container(position_M1,1,1,"M1");
		les_container[0] = M1;
		M2 = new container(position_M2,2,1,"M2");
		les_container[1] = M2;

		//Les bioreacteurs 
		BR1 = new container(position_BR1,1,2,"BR1");
		les_container[2] = BR1;
		BR2 = new container(position_BR2,2,2,"BR2");
		les_container[3] = BR2;
		BR3 = new container(position_BR3,3,2,"BR3");
		les_container[4] = BR3;

		//Les buffer
		BU1 = new container(position_BU1,1,3,"BU1");
		les_container[5] = BU1;
		BU2 = new container(position_BU2,2,3,"BU2");
		les_container[6] = BU2;
		BU3 = new container(position_BU3,3,3,"BU3");
		les_container[7] = BU3;

		AQ = new container(position_AQ,1,4,"AQ");
		les_container[8] = AQ;
		S = new container(position_S,1,5,"S");
		les_container[9] = S;
		
		//On fabrique les pompes :
		les_pompes = new pompe[14];
		//Pompe(float un_x, float un_y, int un_numero ,container cont_pomp,container cont_refoul){
		les_pompes[0] = new pompe(position_BR1[0], (float) (position_BR1[1] - 0.05/2), M1, BR1);
		les_pompes[1] = new pompe(position_BR2[0], (float) (position_BR2[1] - 0.05/2), M1, BR2);
		les_pompes[2] = new pompe(position_BR3[0], (float) (position_BR3[1] - 0.05/2), M1, BR3);
		les_pompes[3] = new pompe(position_BU1[0], (float) (position_BU1[1] - 0.05/2), BR1, BU1);
		les_pompes[4] = new pompe(position_BU2[0], (float) (position_BU2[1] - 0.05/2), BR2, BU2);
		les_pompes[5] = new pompe(position_BU3[0], (float) (position_BU3[1] - 0.05/2), BR3, BU3);
		les_pompes[6] = new pompe(position_BU1[0], (float) (position_AQ[1] - 0.05/2), BU1, AQ);
		les_pompes[7] = new pompe(position_BU2[0], (float) (position_AQ[1] - 0.05/2), BU2, AQ);
		les_pompes[8] = new pompe(position_BU3[0], (float) (position_AQ[1] - 0.05/2), BU3, AQ);
		les_pompes[9] = new pompe((float) 0.6, (float) (position_BR1[1] - 0.05/2), M2, BU1);
		les_pompes[10] = new pompe((float) 0.7, (float) (position_BR1[1] - 0.05/2), M2, BU2);
		les_pompes[11] = new pompe((float) 0.8, (float) (position_BR1[1] - 0.05/2), M2, BU3);
		les_pompes[12] = new pompe((float) 0.9, (float) (position_BR1[1] - 0.05/2), M2, AQ);
		les_pompes[13] = new pompe(position_S[0], (float) (position_S[1] - 0.05/2), AQ, S);
		
		
	

		//frequence de rafrichissement : 
		float frequence = 25;
		frameRate(frequence);//rafraichissement une image toute les 1/25 = 40ms 
		// = (float) 1/frequence; // en s ! 



		//PARIE PARAMETRABLE\\
		
		///////////////\\\\\\\\\\\\\\\
		//Volume réel des trucs litre\\
		//\\\\\\\\\\\\\\\////////////////

		//On met certain container avec un volume initial
		M1.set_volume((float) (1));
		M2.set_volume((float) (1));
		
		AQ.set_volume((float) (0));
		BR1.set_volume((float) (1));
		BR2.set_volume((float) (0));
		BR3.set_volume((float) (0));
		
		BU1.set_volume((float) (1));
		
		//Etat du cycle de chacun des bioreacteurs : Les Trois cycles sont decalés 
		time_hour_C1 = 0;
		time_hour_C2 = 72;
		time_hour_C3 = 144;
		
		
		///////////////\\\\\\\\\\\\\\\
		//\\\\\\\\\\\\\\\///////////////

		currenttime = millis();
		oldtime = millis();;
		
		//Initialisation : 
		/*reader = createWriter("Init.txt"); 
		for (int i = 0 ; i < 14)
		try {
			line = reader.readLine();
		} catch (IOException e) {
			e.printStackTrace();
			line = null;
		}
		switch(t) {
			case 1: 
			
			
			
			break;
			case 2: 
			
			break;
			case 3: 
			
			break;
			case 4: 
			

			break;
			case 5: 
			
		
			break;
		}
		println(line);*/
		
		
		time_start_year = year();
		time_start_month = month();
		time_start_day = day();
		time_start_hour = hour();
		time_start_minute = minute(); 
		time_start_second = second() ;
		
		//!\\Début du code concernant les cycles BR/BU
		
		

		occupied = false;

	 	//Action deja effectuées : BR1_filled_M1 : remplissage de BR1 par M1
		BR1_filled_M1 = false ; 
		BU1_filled_BR1 = false ;
		BU1_filled_M2 = false ;
		BU1_empty = false;

		P_BR1_BU1 = 10;
		P_M1_BR1 = 11;
		P_BU1_AQ = 12;
		P_M2_BU1 = 13;

		//!\\ Beware, new definitions
		AQ_filled_BU1 =  new boolean[24];
		for (int i=0 ; i < AQ_filled_BU1.length;i++) {
			AQ_filled_BU1[i] = false;
		}

		number_time_BU1_used = 0;
		number_time_BU2_used = 0;
		number_time_BU3_used = 0;

		start_step_0 = true;
		start_step_1 = true;
		start_step_2 = true;
		start_step_3 = true;
		start_step_4 = true;
		start_step_5 = true;
		start_step_6 = true;
		start_step_7 = true;

		writer_end = createWriter("log_end.txt");

		//Lecture du fichier log : 
		read_log();


	}

	public void draw(){

		//Permet de connaitre le time entre deux rafraichissement et de calculer le volume debité en conséquence : 
		currenttime = millis();    
		//Temps entre chaque itération en seconde : 
		time_rate = (0.001*(currenttime - oldtime)) ;//en seconde
		oldtime = currenttime;
		
		//Gestion du time : 
		time_second += time_rate;





		if (compteur_log > 300){
			write_log();
			compteur_log = 0;
		}
		compteur_log += 1;
		
		
		if( time_second > 60 ){
			time_minute += time_second / 60;
			time_second = 0;
		}



		if (time_minute > 60 ){
			time_hour_C1 += time_minute / 60;
			//time_hour_C2 += time_minute / 60;
			//time_hour_C3 += time_minute / 60;
			time_minute = 0 ; 
		}

		//Remise à zero des compteurs de cycle : 
		if (time_hour_C1 > 216){
			time_hour_C1 =0;
		}
		/*
		if (time_hour_C2 > 216){
			time_hour_C2 =0;
		}
		if (time_hour_C3 > 216){
			time_hour_C3 =0;
		}*/
		println("time_sec "+time_second);
		println("time_minute "+time_minute);
		println("time_state_1_Hours "+time_hour_C1);
		if (!occupied){
		//Decoupge en plage de cycle : 

		//0 - 3 jours : WAIT
			if(time_hour_C1 <72){
				state_cycle_C1 = 1;
				println("wait");
				BU1_empty = false; 
			}
		//3 - 6  jours : USE
			else if(time_hour_C1 < 144){
				state_cycle_C1 = 2;
				println("use");
				//On met les variable de remplissage à false. 
				BR1_filled_M1 = false ; 
				BU1_filled_BR1 = false ;
				BU1_filled_M2 = false ;
			}
		//6 - 9  jours : EMPTY
			else if(time_hour_C1 < 216){
				state_cycle_C1 = 3;
				println("empty");

				//
				for (int i=0;i < AQ_filled_BU1.length;i++) {
					AQ_filled_BU1[i] = false;
				}
				number_time_BU1_used = 0;
				start_step_0 = true;
				start_step_1 = true;
				start_step_2 = true;
				start_step_3 = true;
				start_step_4 = true;
				start_step_5 = true;
				start_step_6 = true;
				start_step_7 = true;
			}
		}
		
		

		switch (state_cycle_C1) {
			case 1 :
			if (!BU1_filled_BR1) {
				if (BU1.volume_occ < 0.66) {
					arduino.digitalWrite(P_BR1_BU1, arduino.HIGH);
					get_pompe("P_BR1_BU1").state = true;
					occupied = true;		
				}
				else{
					arduino.digitalWrite(P_BR1_BU1, arduino.LOW);
					get_pompe("P_BR1_BU1").state = false;
					BU1_filled_BR1 = true; 					
				}	
			}
			else if (!BU1_filled_M2) {
				if (BU1.volume_occ < 1) {
					arduino.digitalWrite(P_M2_BU1, arduino.HIGH);
					get_pompe("P_M2_BU1").state = true;
				}
 				else {						//problème de l'inégalité, autorise e dépassement!!
 				arduino.digitalWrite(P_M2_BU1, arduino.LOW);
 				get_pompe("P_M2_BU1").state = false;
 				BU1_filled_M2 = true; 									// plus occupé lorsque BU remplit!
 			}	 				
 		}
 		else if (!BR1_filled_M1) {
 			if (BR1.volume_occ < 1) {
 				arduino.digitalWrite(P_M1_BR1, arduino.HIGH);
 				get_pompe("P_M1_BR1").state = true;
 			}
 				else {						//problème de l'inégalité, autorise e dépassement!!
 				arduino.digitalWrite(P_M1_BR1, arduino.LOW);
 				get_pompe("P_M1_BR1").state = false;
 				BR1_filled_M1 = true; 	
 				occupied = false;								// plus occupé lorsque BU remplit!
 			}	 				
 		}

 		break;
 		case 2 :
 		if (!occupied) {
 			if (hour() >= 23 || hour() < 7) { 
 				step = 8;
 				//algaes are breathing, nothing to do 				
 			}else if (hour() >= 21) {
 				step = 7;
 				if (start_step_7) {
 					number_time_BU1_used += 1 ;
 					start_step_7 = false;
 					start_step_6 = true;
 				}
 			}else if (hour() >= 19) {
 				step = 6;
 				if (start_step_6) {
 					number_time_BU1_used += 1 ;
 					start_step_6 = false;
 					start_step_5 = true;
 				}
 			}else if (hour() >= 17) {
 				step = 5;
 				if (start_step_5) {
 					number_time_BU1_used += 1 ;
 					start_step_5 = false;
 					start_step_4 = true;
 				}
 			}else if (hour() >= 15) {
 				step = 4;
 				if (start_step_4) {
 					number_time_BU1_used += 1 ;
 					start_step_4 = false;
 					start_step_3 = true;
 				}
 			}else if (hour() >= 13) {
 				step = 3;
 				if (start_step_3) {
 					number_time_BU1_used += 1 ;
 					start_step_3 = false;
 					start_step_2 = true;
 				}
 			}else if (hour() >= 11) {
 				step = 2;
 				if (start_step_2) {
 					number_time_BU1_used += 1 ;
 					start_step_2 = false;
 					start_step_1 = true;
 				}
 			}else if (hour() >= 9) {
 				step = 1;
 				if (start_step_1) {
 					number_time_BU1_used += 1 ;
 					start_step_1 = false;
 					start_step_0 = true;
 				}
 			}else if (hour() >= 7) {
 				step = 0;
 				if (start_step_0) {
 					number_time_BU1_used += 1 ;
 					start_step_0 = false;
 					start_step_7 = true;
 				}
 			}
 			println(step);
 			println(hour());
 		}
 		switch(step) {
 			case 7:
 			if (!AQ_filled_BU1[number_time_BU1_used -1]){
 				if ((BU1.volume-BU1.volume_occ*BU1.volume)/(number_time_BU1_used) < (BU1.volume/24)){
 					arduino.digitalWrite(P_BU1_AQ, arduino.HIGH);
 					get_pompe("P_BU1_AQ").state = true;
 					occupied = true;

 				}else{
 					arduino.digitalWrite(P_BU1_AQ, arduino.LOW);
 					get_pompe("P_BU1_AQ").state = false;
 					AQ_filled_BU1[number_time_BU1_used -1] = true;
 					occupied = false;
 				}
 			}
 			break;
 			case 6:
 			if (!AQ_filled_BU1[number_time_BU1_used-1]){
 				if ((BU1.volume-BU1.volume_occ*BU1.volume)/(number_time_BU1_used) < (BU1.volume/24)){
 					arduino.digitalWrite(P_BU1_AQ, arduino.HIGH);
 					get_pompe("P_BU1_AQ").state = true;
 					occupied = true;
 				}else{
 					arduino.digitalWrite(P_BU1_AQ, arduino.LOW);
 					get_pompe("P_BU1_AQ").state = false;
 					AQ_filled_BU1[number_time_BU1_used-1] = true;
 					occupied = false;
 				
 					
 				}
 			}
 			break;
 			case 5:
 			if (!AQ_filled_BU1[number_time_BU1_used-1]){
 				if ((BU1.volume-BU1.volume_occ*BU1.volume)/(number_time_BU1_used) < (BU1.volume/24)){
 					arduino.digitalWrite(P_BU1_AQ, arduino.HIGH);
 					get_pompe("P_BU1_AQ").state = true;
 					occupied = true;
 				}else{
 					arduino.digitalWrite(P_BU1_AQ, arduino.LOW);
 					get_pompe("P_BU1_AQ").state = false;
 					AQ_filled_BU1[number_time_BU1_used -1] = true;
 					occupied = false;
 				}
 			}
 			break;
 			case 4:
 			if (!AQ_filled_BU1[number_time_BU1_used-1]){
 				if ((BU1.volume-BU1.volume_occ*BU1.volume)/(number_time_BU1_used) < (BU1.volume/24)){
 					arduino.digitalWrite(P_BU1_AQ, arduino.HIGH);
 					get_pompe("P_BU1_AQ").state = true;
 					occupied = true;
 				}else{
 					arduino.digitalWrite(P_BU1_AQ, arduino.LOW);
 					get_pompe("P_BU1_AQ").state = false;
 					AQ_filled_BU1[number_time_BU1_used-1] = true;
 					occupied = false;
 				}
 			}
 			break;
 			case 3:
 			if (!AQ_filled_BU1[number_time_BU1_used-1]){
 				if ((BU1.volume-BU1.volume_occ*BU1.volume)/(number_time_BU1_used) < (BU1.volume/24)){
 					arduino.digitalWrite(P_BU1_AQ, arduino.HIGH);
 					get_pompe("P_BU1_AQ").state = true;
 					occupied = true;
 				}else{
 					arduino.digitalWrite(P_BU1_AQ, arduino.LOW);
 					get_pompe("P_BU1_AQ").state = false;
 					AQ_filled_BU1[number_time_BU1_used-1] = true;
 					occupied = false;
 				}
 			}
 			break;
 			case 2:
 			if (!AQ_filled_BU1[number_time_BU1_used-1]){
 				if ((BU1.volume-BU1.volume_occ*BU1.volume)/(number_time_BU1_used) < (BU1.volume/24)){
 					arduino.digitalWrite(P_BU1_AQ, arduino.HIGH);
 					get_pompe("P_BU1_AQ").state = true;
 					occupied = true;
 				}else{
 					arduino.digitalWrite(P_BU1_AQ, arduino.LOW);
 					get_pompe("P_BU1_AQ").state = false;
 					AQ_filled_BU1[number_time_BU1_used-1] = true;
 					occupied = false;
 				}
 			}
 			break;
 			case 1:
 			if (!AQ_filled_BU1[number_time_BU1_used-1]){
 				if ((BU1.volume-BU1.volume_occ*BU1.volume)/(number_time_BU1_used) < (BU1.volume/24)){
 					arduino.digitalWrite(P_BU1_AQ, arduino.HIGH);
 					get_pompe("P_BU1_AQ").state = true;
 					occupied = true;
 				}else{
 					arduino.digitalWrite(P_BU1_AQ, arduino.LOW);
 					get_pompe("P_BU1_AQ").state = false;
 					AQ_filled_BU1[number_time_BU1_used-1] = true;
 					occupied = false;
 				}
 			}
 			break;
 			case 0:
 			if (!AQ_filled_BU1[number_time_BU1_used-1]){
 				if ((BU1.volume-BU1.volume_occ*BU1.volume)/(number_time_BU1_used) < (BU1.volume/24)){
 					arduino.digitalWrite(P_BU1_AQ, arduino.HIGH);
 					get_pompe("P_BU1_AQ").state = true;
 					occupied = true;
 				}else{
 					arduino.digitalWrite(P_BU1_AQ, arduino.LOW);
 					get_pompe("P_BU1_AQ").state = false;
 					AQ_filled_BU1[number_time_BU1_used-1] = true;
 					occupied = false;
 				}
 			}
 			break;
 		}

 		break;
 		case 3 :
 		if (!BU1_empty) {
				if (BU1.volume_occ > 0) {
					arduino.digitalWrite(P_BU1_AQ, arduino.HIGH);
					get_pompe("P_BU1_AQ").state = true;
					occupied = true;		
				}
				else{
					arduino.digitalWrite(P_BU1_AQ, arduino.LOW);
					get_pompe("P_BU1_AQ").state = false;
					BU1_empty = true; 
					occupied = false; 					
				}	
			}
 		break;

 	}







		//Gestion des niveaux des differents container suivant l'etat des pompes 
 	for (int j =0; j <les_pompes.length; j++ ){
 		if (les_pompes[j].state){

 			if (les_pompes[j].container_pomp.volume_occ>0){
 				les_pompes[j].container_pomp.vider();
 				les_pompes[j].container_refoul.remplir();
 			}

 		}
 	}








		//On met à jour l'interface graphique 
 	dessiner();	
 }





 public void Print_visual(String S){

 	fill(0,0,0);
 	noStroke();
 	rect(share_visual_x*width,0,(float) (1-share_visual_x)*width,(float) 1*height );
 	fill(255,255,255);
 	text(S, (share_visual_x+(1-share_visual_x)*0.2)*width, (float) (height/2));

 }



	//Get pompe d'après son nom
 public pompe get_pompe(String S){
 	pompe  P = null;  
 	for (int i =0 ; i < les_pompes.length ; i++){
 		if( les_pompes[i].name.equals(S)){
 			P = les_pompes[i];
 		}			
 	}
 	return P;
 }
	//Get container d'après son nom
 public container get_container(String S){
 	container  C = null;  
 	for (int i =0 ; i < les_container.length ; i++){
 		if( les_container[i].name.equals(S)){
 			C = les_container[i];
 		}			
 	}
 	return C;
 }






	//Action interaction utilisateur
 public void keyPressed() {
		//println(key);
 	int s = Character.getNumericValue(key);
 }
 public void mousePressed(){

 }


	//Dessine tous les containers, les tuyaux et les pompes.    
 public void dessiner(){
 	background(150);
		//Dessine les tuyaux
 	for (int i = 0 ; i<les_pompes.length; i++){
 		les_pompes[i].dessiner_tuyau();
 	}
		//Dessine les tuyaux
 	for (int i = 0 ; i<les_pompes.length; i++){
 		if (!les_pompes[i].state) les_pompes[i].dessiner_pompe();
 	}
		//colorie en Vert les pompes et tuyaux en action
 	for (int i = 0 ; i<les_pompes.length; i++){
 		if (les_pompes[i].state){
 			les_pompes[i].dessiner_pompe();
 			les_pompes[i].dessiner_tuyau();
 		}

 	}
		//dessine les container 
 	for (int i = 0 ; i<les_container.length; i++){
 		les_container[i].dessiner();
 	}


 }
 public class container{
		//Position
 	float[] Position;
 	float x;
 	float y; 

		//taille en pourcentage de la taille de la fenetre 
 	float largeur;
 	float hauteur;

		//Remplissage en pourcentage 
 	float volume_occ;
 	float volume;
		//Concentration en pourcentage
 	float concentration = 1;
		//Numero du récipient;
 	int le_numero;
 	String name;

		//Type de container : 1 Milieu de culture ; 2 Bioreacteur ; 3 Buffer ; 4 Aquarium ; 5 stockage 
 	int type;

		//Pompes 
		pompe[] pompes; //Nombre variable en fonction du type 
		
		//Electrodes : 
		boolean[] EL_state;
		float[] EL_position;
		
		
		//Container(position, numero, type, nom)
		container(float[] P, int un_numero, int t,String N){
			Position = P;
			x = Position[0];
			y = Position[1];
			le_numero = un_numero;
			type = t; 
			concentration = (float) 0.8;//A la base, concentration a 0.8;
			name = N;

			switch(t) {
				case 1: 
				// Cas d'un Milieu de cuture 
				largeur = dimension_M[0];
				hauteur = dimension_M[1];
				volume=volume_M;

				EL_state = new boolean[EL_M.length];
				for (int i =0 ; i<EL_state.length ; i++){
					EL_state[i]= false;
				}

				EL_position = EL_M;

				break;
				case 2: 
				// Cas d'un bioreacteur 
				largeur = dimension_BR[0];
				hauteur = dimension_BR[1];
				volume=volume_BR;

				EL_state = new boolean[EL_BR.length];
				for (int i =0 ; i<EL_state.length ; i++){
					EL_state[i]= false;
				}

				EL_position = EL_BR;
				break;
				case 3: 
				// Cas d'un Buffer 
				largeur = dimension_BU[0];
				hauteur = dimension_BU[1];
				volume=volume_BU;

				EL_state = new boolean[EL_BU.length];
				for (int i =0 ; i<EL_state.length ; i++){
					EL_state[i]= false;
				}

				EL_position = EL_BU;



				break;
				case 4: 
				// Cas d'un aquarium 
				largeur = dimension_AQ[0];
				hauteur = dimension_AQ[1];
				volume=volume_AQ;

				EL_state = new boolean[EL_AQ.length];
				for (int i =0 ; i<EL_state.length ; i++){
					EL_state[i]= false;
				}

				EL_position = EL_AQ;

				break;
				case 5: 
				// Cas d'un stockage
				largeur = dimension_S[0];
				hauteur = dimension_S[1];
				volume=volume_S;


				EL_state = new boolean[EL_S.length];
				for (int i =0 ; i<EL_state.length ; i++){
					EL_state[i]= false;
				}
				EL_position = EL_S;

				break;
			}

		}

		//Set volum demandé dans le container / met à jour l'etat des EL
		void set_volume(float un_volume){
			volume_occ = un_volume;

			//Electrodes : On detecte si l'electrode touche ou non, et on met EL_state à jour en consequence
			for(int i=0 ; i<EL_position.length ; i++ ){
				EL_state[i] = (volume_occ >= EL_position[i]);		  
			}

		}
		void remplir(){
			//time est en s ! 
			float v = (float) ((time_rate*debit_pompe)/(60*volume));
			set_volume( volume_occ+ v) ;//En pourcentage (0-1)






		}
		void vider(){
			//time est en s ! 
			float v = (float) ((time_rate*debit_pompe)/(60*volume));
			set_volume( volume_occ - v) ;//En pourcentage (0-1)
		}

		void dessiner(){
			//Container :  
			//structure vide 
			stroke(0);
			fill(0,0,0);
			rect(Position[0]*width*share_visual_x,Position[1]*height*share_visual_y,width*share_visual_x*largeur,height*share_visual_y*hauteur);
			//structure remplie
			noStroke();
			if (type == 1){
				fill(255,255,255);
			}
			else fill(0,255,0);
			rect(Position[0]*width*share_visual_x,Position[1]*height*share_visual_y+(height*share_visual_y*hauteur)*(1-volume_occ),width*share_visual_x*largeur,(height*share_visual_y*hauteur)*volume_occ);
			//Electrode : 
			for(int i = 0 ; i<EL_state.length ; i++ ){
				noStroke();
				if (EL_state[i]) {
					fill(0,0,255);
				}
				else {
					fill(255,0,0);
				}
				rect(Position[0]*width*share_visual_x,Position[1]*height*share_visual_y+(height*share_visual_y*hauteur)*(1-EL_position[i]),width*share_visual_x*largeur,height*share_visual_y*hauteur*0.01);			  	  
			}





		}  
		public void set_concentration(float uneC){
			concentration = uneC; 
		}

	}


	public class pompe{
		//Position
		float  x;
		float  y; 
		//taille en pourcentage de la taille de la fenetre 
		float largeur =(float) 0.03;
		float hauteur=(float) 0.03;

		//Nom
		String name;
		//Etat
		boolean state ; 

		//Numero de la pompe;
		int le_numero;

		//Points de ratache aux recipients :(une pompe relie toujours 2 points.  
		float[] point_attache_pomp;
		float[] point_attache_refoul;

		//container 
		container container_pomp;//de pompage
		container container_refoul;//de refoulement



		//postion de la pompe : un_x, un_y 
		//P1 : postion du point d'accroche 1 
		//P2 postion du point d'accroche 2
		//pompe : container_1->container_2 

		//pompe(float un_x, float un_y, int un_numero ,float[] P1,float[] P2, int type ){
		pompe(float un_x, float un_y, container cont_pomp, container cont_refoul){

			x = un_x;
			y = un_y; 
			//le_numero = un_numero;
			state = false;


			container_pomp = cont_pomp;//de pompage
			container_refoul = cont_refoul;//de refoulement

			name = "P_"+container_pomp.name +"_"+container_refoul.name;
			point_attache_pomp = new float[2] ;
			point_attache_pomp[0] = cont_pomp.Position[0];
			point_attache_pomp[1] = cont_pomp.Position[1]+ 0.16;

			point_attache_refoul = new float[2] ;
			point_attache_refoul[0] = cont_refoul.Position[0];
			point_attache_refoul[1] = cont_refoul.Position[1];






		}
		//Set les container de pompage et refoulement, Nomme la pompe correspondant suivant la syntaxe : P"Container_Pompage"-"Container_refoul" ex : PM1-BR1
		void set_pompe (container cont_pomp,container cont_refoul){
			//container 
			container_pomp = cont_pomp;//de pompage
			container_refoul = cont_refoul;//de refoulement

			name = "P"+container_pomp.name +"_"+container_refoul.name;



		}


		//dessine le chemin de la pompe
		void dessiner_tuyau(){

			if (state){
				if (container_pomp.type == 1){
					stroke (255,255,255);
				}
				else {
					stroke(0,255,0);	
				}
			}
			else stroke(0,0,0);

			strokeWeight(5);
			strokeCap(SQUARE);
			line(x*width*share_visual_x,y*height*share_visual_y, point_attache_pomp[0]*width*share_visual_x, y*height*share_visual_y);
			line(point_attache_pomp[0]*width*share_visual_x,y*height*share_visual_y, point_attache_pomp[0]*width*share_visual_x, point_attache_pomp[1]*height*share_visual_y);

			strokeWeight(5);
			strokeCap(SQUARE);
			line(x*width*share_visual_x,y*height*share_visual_y, x*width*share_visual_x, point_attache_refoul[1]*height*share_visual_y);
			line(x*width*share_visual_x, point_attache_refoul[1]*height*share_visual_y, point_attache_refoul[0]*width*share_visual_x, point_attache_refoul[1]*height*share_visual_y);


		}
		//On dessine la pompe
		void dessiner_pompe(){
			stroke(0);
			if (state){
				if (container_pomp.type == 1){
					fill (255,255,255);
				}
				else {
					fill(0,255,0);	
				}
			}
			else fill(255,0,0);
			ellipse(x*width*share_visual_x,y*height*share_visual_y,width*share_visual_x*largeur,height*share_visual_y*hauteur);
		}
		void set_state(boolean B){
			state = B;
			
		}
	}
	public void save_log(){

	}

public void read_log(){
	reader = createReader("log_start.txt");
	String line; 
	String[] info;
	int num_line = 0;
	try {
		line = reader.readLine();
	} catch (IOException e) {
		e.printStackTrace();
		line = null;
	}

	while (line!=null){
		println(line);
		info = split(line,":");
		switch (num_line) {
			case 0 : 
			time_hour_C1 = float(info[1]);
			break; 

			case 1 : 
			time_hour_C2 = float(info[1]);
			break;  

			case 2 : 
			time_hour_C3 = float(info[1]);
			break;  

			case 3 : 
			M1.set_volume(float(info[1]));
			break;  

			case 4 : 
			M2.set_volume(float(info[1]));
			break;  

			case 5 : 
			BR1.set_volume(float(info[1]));
			break; 

			case 6 : 
			BR2.set_volume(float(info[1]));
			break;  

			case 7 : 
			BR3.set_volume(float(info[1]));
			break; 

			case 8 : 
			BU1.set_volume(float(info[1]));
			break;  

			case 9 : 
			BU2.set_volume(float(info[1]));
			break;  

			case 10 : 
			BU3.set_volume(float(info[1]));
			break;  

			case 11 :
			AQ.set_volume(float(info[1]));
			break;

			case 12 : 
			S.set_volume(float(info[1]));
			break;  

			case 13 : 
			number_time_BU1_used = int(info[1]);
			break;  

			case 14 : 
			number_time_BU2_used = int(info[1]);
			break; 

			case 15 : 
			number_time_BU3_used = int(info[1]);
			break; 


		}
		num_line += 1;
		try {
			line = reader.readLine();
		} catch (IOException e) {
			e.printStackTrace();
			line = null;
		}

	} 

}
public void write_log(){
	println("Saving_state");
	writer_end.println("cycle C1 (0-72 = wait / 72-144 = use / 144-216 = empty) : " + time_hour_C1 );
	writer_end.println("cycle C2 (0-72 = wait / 72-144 = use / 144-216 = empty) : " + time_hour_C2 );
	writer_end.println("cycle C3 (0-72 = wait / 72-144 = use / 144-216 = empty) : " + time_hour_C3 );
	writer_end.println("volume M1 occ (pourcentage): " + M1.volume_occ );
	writer_end.println("volume M2 occ (pourcentage): " + M2.volume_occ );
	writer_end.println("volume BR1 occ (pourcentage): " + BR1.volume_occ );
	writer_end.println("volume BR2 occ (pourcentage): " + BR2.volume_occ );
	writer_end.println("volume BR3 occ (pourcentage): " + BR3.volume_occ );
	writer_end.println("volume BU1 occ (pourcentage): " + BU1.volume_occ );
	writer_end.println("volume BU2 occ (pourcentage): " + BU2.volume_occ );
	writer_end.println("volume BU3 occ (pourcentage): " + BU3.volume_occ );
	writer_end.println("volume AQ occ (pourcentage): " + AQ.volume_occ );
	writer_end.println("volume S occ (pourcentage): " + S.volume_occ );
	writer_end.println("number_time_BU1_used : " + number_time_BU1_used);
	writer_end.println("number_time_BU2_used : " + number_time_BU2_used);
	writer_end.println("number_time_BU3_used : " + number_time_BU3_used);
	writer_end.println("time_end :" +  hour() + ":" +minute() + ":" +second() + "   " + day() + "/" + month() +"/" + year());
	writer_end.println("time_start :" +  time_start_hour + ":" +time_start_minute + ":" +time_start_second + "   " + time_start_day + "/" + time_start_month +"/" + time_start_year);

    writer_end.println();

    writer_end.flush();

    writer_start = createWriter("log_start.txt");

    writer_start.println("cycle C1 (0-72 = wait / 72-144 = use / 144-216 = empty) : " + time_hour_C1 );
	writer_start.println("cycle C2 (0-72 = wait / 72-144 = use / 144-216 = empty) : " + time_hour_C2 );
	writer_start.println("cycle C3 (0-72 = wait / 72-144 = use / 144-216 = empty) : " + time_hour_C3 );
	writer_start.println("volume M1 occ (pourcentage): " + M1.volume_occ );
	writer_start.println("volume M2 occ (pourcentage): " + M2.volume_occ );
	writer_start.println("volume BR1 occ (pourcentage): " + BR1.volume_occ );
	writer_start.println("volume BR2 occ (pourcentage): " + BR2.volume_occ );
	writer_start.println("volume BR3 occ (pourcentage): " + BR3.volume_occ );
	writer_start.println("volume BU1 occ (pourcentage): " + BU1.volume_occ );
	writer_start.println("volume BU2 occ (pourcentage): " + BU2.volume_occ );
	writer_start.println("volume BU3 occ (pourcentage): " + BU3.volume_occ );
	writer_start.println("volume AQ occ (pourcentage): " + AQ.volume_occ );
	writer_start.println("volume S occ (pourcentage): " + S.volume_occ );
	writer_start.println("number_time_BU1_used : " + number_time_BU1_used);
	writer_start.println("number_time_BU2_used : " + number_time_BU2_used);
	writer_start.println("number_time_BU3_used : " + number_time_BU3_used);
	writer_start.println("time_end :" +  hour() + ":" +minute() + ":" +second() + "   " + day() + "/" + month() +"/" + year());
	writer_start.println("time_start :" +  time_start_hour + ":" +time_start_minute + ":" +time_start_second + "   " + time_start_day + "/" + time_start_month +"/" + time_start_year);  

	writer_start.println();

    writer_start.flush();
    writer_start.close();
}



