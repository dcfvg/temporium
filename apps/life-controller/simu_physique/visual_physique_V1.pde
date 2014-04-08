import processing.serial.*;

  float share_visual_x;
  float share_visual_y;  

  
  int i ;

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
  int test ; 
  
  //Communication
  Serial myPort;  // Create object from Serial class
  boolean firstContact ;
  String msg;
   
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
  
  //temps entre deux rafraichissement;
  float temps; 
  int currenttime;
  int oldtime;

  int compteur;
  
  //Tache demandées : 
 
  boolean filling_BR1;//a
  boolean filling_BR2;//z
  boolean filling_BR3;//e
  
  boolean filling_BU1;//r
  boolean filling_BU2;//t
  boolean filling_BU3;//y
  
  boolean filling_AQ_BU1;//u 
  boolean filling_AQ_BU2;
  boolean filling_AQ_BU3;
  
  boolean emptying_AQ;//i
  
  boolean[] Action_state;
  
  String task_asked;
  String task_executed; 
  
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

    //on initialise la partie visuelle 
    share_visual_x = 0.7;
    share_visual_y = 1; 

	//Communcation
	firstContact = false;
    myPort = new Serial(this, Serial.list()[2], 9600);
	//println(Serial.list());
    myPort.bufferUntil('\n'); 
	
	//Electrodes : Nombre et place des electrodes dans chaque type de container 

	EL_M = new float[1];
	EL_M[0] = 0.05 ; //EL a 5% du fond. 
	
	EL_BR = new float[3];
	EL_BR[0] = 0.10 ; //10%
	EL_BR[1] = 0.55 ; //55%
	EL_BR[2] = 1 ; //100%
	
	EL_BU = new float[3];
	EL_BU[0] = 0.01 ; //1%
	EL_BU[1] = 0.50 ; //50%
	EL_BU[2] = 1 ; //100%
	
	EL_AQ = new float[3];
	EL_AQ[0] = 0.01 ; //1%
	EL_AQ[1] = 0.9 ; //0.6875 ; //68,75% car, aq 8L , donc vidage de 2,5L a chaque fois.  
	EL_AQ[2] = 1 ; //100%
	
	EL_S = new float[1];
	EL_S[0] = 0.9 ; //90%
	


	// on initialise l'etat des actions : 
	Action_state = new boolean[10];
	
	filling_BR1 = false;
	Action_state[0] = filling_BR1;
	filling_BR2 = false;
	Action_state[1] = filling_BR2;
	filling_BR3 = false;
	Action_state[2] = filling_BR3;
  	
	filling_BU1 = false;
	Action_state[3] = filling_BU1;
	filling_BU2 = false;
	Action_state[4] = filling_BU2; 	
	filling_BU3 = false;
	Action_state[5] = filling_BU3;
  
	filling_AQ_BU1 = false; 
	Action_state[6] = filling_AQ_BU1;
	filling_AQ_BU2 = false; 
	Action_state[7] = filling_AQ_BU2;
	filling_AQ_BU3 = false; 
	Action_state[8] = filling_AQ_BU3;

	emptying_AQ = false;
	Action_state[9] = emptying_AQ;
	
	task_asked = "NULL";
	task_executed = "NULL";
	
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

    //Volume réel des trucs litre
    volume_M = (float) 10; 
    volume_BR =(float) 1.6  ;
    volume_BU =(float) 1.6  ;
    volume_AQ =(float) 2.5;
    volume_S = (float) 1;


    
    
    compteur=0;

    test = 0;

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
	//On initialise les pompes : 
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
	
	
    i = 0;

    //frequence de rafrichissement : 
    float frequence = 25;
    frameRate(frequence);//rafraichissement une image toute les 1/25 = 40ms 
    temps = (float) 1/frequence; // en s ! 
    //Debit pompe : 
    debit_pompe = (float) 1;//en L/min
   
   
    //On met les differents container à 0 en volume. 
    for (int i = 0; i< les_container.length; i++){
      les_container[i].set_volume((float) 0);
    }
	//On met certain container avec un volume initial
    M1.set_volume((float) (1));
    M2.set_volume((float) (1));
	
	AQ.set_volume((float) (1));
    BR1.set_volume((float) (1));
    BR2.set_volume((float) (1));
    BR3.set_volume((float) (1));
	
	BU1.set_volume((float) (1));
   
    currenttime = millis();
    oldtime = millis();;
	
	//Buffer USED
	BU_USED = "BU1" ;

  }

  public void draw(){
  	//Permet de connaitre le temps entre deux rafraichissement et de calculer le volume debité en conséquence : 
	
  	currenttime = millis();    
	//println("temps_vrai" + (0.001*(currenttime - oldtime))); 
  	temps = (0.001*(currenttime - oldtime));
	
	oldtime = currenttime;

    //on modifie les niveaux des different
    for (int j =0; j <les_pompes.length; j++ ){
      if (les_pompes[j].state){
		  
        if (les_pompes[j].container_pomp.volume_occ>0){
          les_pompes[j].container_pomp.vider();
          les_pompes[j].container_refoul.remplir();
        }

      }
    }
	
    //on lit le msg envoyé par l'arduino
     /*if ( myPort.available() > 0) 
    {  
    msg = myPort.readStringUntil('\n');  // read it and store it in val A COMPLETER 
    } 
	//println(msg);
	
	//On effectue l'action associée au msg
	//action_Arduino(msg);
	*/
     
	 
    dessiner();
	
  }
  //Appelé lorsqu'un donnée est disponible sur le port serie : 
  public void serialEvent( Serial myPort) {
 	 //put the incoming data into a String - 
  	 //the '\n' is our end delimiter indicating the end of a complete packet
   	 msg = myPort.readStringUntil('\n');
	 
	  
	 
	 
    //make sure our data isn't empty before continuing
	 if (msg != null) {
	 msg = trim(msg);
	 println("Message recu : " + msg);

		 //look for our 'A' string to start the handshake
	     //if it's there, clear the buffer, and send a request for data
	 	if ( !firstContact ) {
     	   if (msg.equals("A")) {
     		  myPort.clear();
     		  firstContact = true;
     		  myPort.write("OK");//ce qui est renvoyé pas important du moment que l'on renvoie qqchose
     		  println("contact established");
     	   }
    	 }
		 
		 //first contact arlready established, msg treatment  : 
		 else {
		 	msg_received(msg);
		 }	 
	 }
  }
  public void msg_received(String msg_r){

    String[] S = split(msg_r,"_");
   
    String msg_send = "OK";
    
	if (S[0].equals("A")){
		//On renvoie "OK"
		msg_send = "OK";
	}
   
   //Info sur etat d'une pompe : du type "P_M1_BR1_ON" 
    if (S[0].equals("P")){
		//On met les pompes dans l'etat indiqué
    	get_pompe(S[0]+"_"+S[1]+"_"+S[2]).set_state(S[3].equals("ON"));
		
		//Envoyer OK pour continuer 
		msg_send = "OK";
    }
    
    //Demande d'info sur une electrode : du type "EL_BR1_1" 
    else if (S[0].equals("EL")){
		
		boolean B = get_container(S[1]).EL_state[Integer.parseInt(S[2])];
		//On envoie le resultat sous la forme : "EL_BR1_1_ON"/ "EL_BR1_1_OFF"
		if(B){
			msg_send = msg_r +"_ON";
		}
		else {
			msg_send = msg_r +"_OFF";
		}
		
    }
    //Demande : ASK_T demande de tache // ASK_K demande de continuer
    else if (S[0].equals("ASK")){
    	
		//Demande de tache
    	if(S[1].equals("T")){
			
			// /!\Exception : tache demandée alors qu'il n'a pas fini la derniere 
			if (!task_executed.equals("NULL")){
				println("WARNING : TASK ASKED , BUT TASK IN PROGRESS ON ARDUINO");
			}
			
    		//On envoie la tache demandée
    		msg_send = task_asked;
    		//Tache demandée à NULL
			task_asked = "NULL";
   		}
		
		
   		//Demande de continuer /!\ Pour l'instant, on dit toujours de continuer
    	if(S[1].equals("K")){
    		//Envoyer OK pour continuer 
    		msg_send=  "OK";
    	}
		
    }
	
	
	//Info de tache sur la tache coté arduino : T_FILLING_BR1_B :tache commancée // T_FILLING_BR1_E : tache terminé ( RQ :T_FILLING_AQBU3_B pour )
	
    else if (S[0].equals("T")){
    	
		//Tache debutée
    	if(S[3].equals("B")){
    		//Tache en cours 
    		task_executed = S[0]+"_"+S[1]+"_"+S[2];
    		//Revoyer OK
    		msg_send = "OK"; 
   		}
   		//tache finie
   		if(S[3].equals("E")){
    		task_executed = "NULL";
    		//Revoyer OK
    		msg_send = "OK"; 
   		}	
    }
    else if (S[0].equals("BU")){
    	
		//Tache debutée
    	if(S[1].equals("PLEASE")){
    		
    		//Revoyer le buffer à utiliser : 
    		msg_send = "BU1"; 
   		}
   		
    }
	println("Messeage envoyé : " + msg_send);
  myPort.write(msg_send +'\n');
  }
  
  //Action déclanchée losrque la touche est frappée
  public void keyPressed() {
  	//println(key);
  	int s = Character.getNumericValue(key);
  	
  	if ( !task_asked.equals("NULL") ){
  		println("tache demandée en attente");
  		}
  	else {
  		if(task_executed.equals("NULL")){  		
	  		switch(s) {
	      case 1: 
	        task_asked ="T_FILLING_BR1";
	        break;
	      
	      case 2: 
	      	task_asked ="T_FILLING_BR2" ;
	        break;
	      
	      case 3: 
	      	task_asked ="T_FILLING_BR3"	;
	        break;
	        
	      case 4: 
	        task_asked ="T_FILLING_BU1";
	        break;
	        
	      case 5: 
	        task_asked ="T_FILLING_BU2"	;
	        break;
	        
	      case 6: 
	        task_asked ="T_FILLING_BU3"	;
	        break;
	        
	      case 7: 
	        task_asked ="T_FILLING_AQ";	
	        break;
	      
		  case 0:
		    task_asked ="T_EMPTYING_AQ";
			break; 
	
	      }
		 
	  }

  	}	
	println("Tache demandée " + task_asked);
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
  
  
  
  public void action_Arduino(String uneString){

    String[] S = split(uneString,"_");

    for (int j =0; j <les_pompes.length; j++ ){
      if (les_pompes[j].name.equals(S[0])){
        if (S[1].equals("ON")){
          les_pompes[j].set_state(true);
        }
        if (S[1].equals("OFF")){
          les_pompes[j].set_state(false);

        }

      }
    }
  }
/*
//Retourne le container à partir de son numéro. 
  public container get_cont(int N){
    String S = numero_cont[N];
    container C = null;
    for (int i = 0 ; i<les_container.length; i++){
      if (les_container[i].name.equals(S)){
        C = les_container[i];
      }
    }
    return C;
  }
  */
  
  
  /*public void mousePressed(){
      for (int i = 0 ; i<les_pompes.length; i++){
       // les_pompes[i].set_state(false);
        msg_received(les_pompes[i].name+"_OFF");
      }  
      //les_pompes[test].set_state(true);
     // System.out.println(les_pompes[test].name);
      msg_received(les_pompes[test].name+"_ON");
      test = (test +1)%14;
    }
    */
    
 //Dessine tous les containers, les tuyaux et les pompes.    
  void dessiner(){
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


    void set_volume(float un_volume){
      volume_occ = un_volume;
	  
	  //Electrodes : On detecte si l'electrode touche ou non, et on met EL_state à jour en consequence
	  for(int i=0 ; i<EL_position.length ; i++ ){
			  EL_state[i] = (volume_occ >= EL_position[i]);		  
	  }
	  
    }
    void remplir(){
		//temps est en s ! 
      float v = (float) ((temps*debit_pompe)/(60*volume));
      set_volume( volume_occ+ v) ;//En pourcentage (0-1)
	  
	  
	  
	  
	  
	  
    }
    void vider(){
		//temps est en s ! 
      float v = (float) ((temps*debit_pompe)/(60*volume));
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
	  Print_visual(les_pompes[test].name);
	  
	
	
	
	
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



