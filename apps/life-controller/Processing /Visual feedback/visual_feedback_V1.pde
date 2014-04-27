import processing.serial.*;

  float share_visual_x;
  float share_visual_y;  

  int oldtime;
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


  float temps; //temps entre deux rafraichissement;

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
  

  public void setup(){
    size(800,700);
    background(150);

    //on initialise la partie visuelle 
    share_visual_x = 0.7;
    share_visual_y = 1; 

//Communcation
	firstContact = false;
    println("Available serial ports:");
    println(Serial.list());
    myPort = new Serial(this, Serial.list()[0], 9600);
    myPort.bufferUntil('\n'); 


	//on initialise l'etat des actions : 
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
	
	task_asked = "null";
	task_executed = "null";
	
    //On initilise les positions (de 0 à 1, en pourcentage de la taille de la fenetre): 

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
    float frequence = 60;
    frameRate(frequence);//rafraichissement une image toute les 40ms
    temps = (float) 1/frequence; 
    //Debit pompe : 
    debit_pompe = (float) 5;//en L/min
   
   
    //On met les differents container à 0 en volume. 
    for (int i = 0; i< les_container.length; i++){
      les_container[i].set_volume((float) 0);

    }
    M1.set_volume((float) (1));
    M2.set_volume((float) (1));
  

  }

  public void draw(){

    //on modifie les niveaux des different
    for (int j =0; j <les_pompes.length; j++ ){
      if (les_pompes[j].state){
        if (les_pompes[j].container_pomp.volume_occ>0 & les_pompes[j].container_refoul.volume_occ<1){
          les_pompes[j].container_pomp.vider();
          les_pompes[j].container_refoul.remplir();
        }

      }
    }
    //on lit le msg envoyé par l'arduino
      if ( myPort.available() > 0) 
    {  
    msg = myPort.readStringUntil('\n');  // read it and store it in val A COMPLETER 
    } 
	//println(msg);
	
	//On effectue l'action associée au msg
	//action_Arduino(msg);
	
     
    dessiner();

  }
  //Action déclanchée losrque la touche est frappée
  void keyPressed() {
  	//println(key);
  	int s = Character.getNumericValue(key);
  	
  	if ( !task_asked.equals("null") ){
  		println("tache demandée en attente");
  		}
  	else {
  		if(task_executed.equals("null")){}
  		
  		
	  		switch(s) {
	      case 1: 
	        task_asked ="T_filling_BR1";
	        break;
	      
	      case 2: 
	      	task_asked ="T_filling_BR2" ;
	        break;
	      
	      case 3: 
	      	task_asked ="T_filling_BR3"	;
	        break;
	        
	      case 4: 
	        task_asked ="T_filling_BU1";
	        break;
	        
	      case 5: 
	        task_asked ="T_filling_BU2"	;
	        break;
	        
	      case 6: 
	        task_asked ="T_filling_BU3"	;
	        break;
	        
	      case 7: 
	        task_asked ="T_filling_AQ_BU1";	
	        break;
	      
	      case 8: 
	        task_asked ="T_filling_AQ_BU2";	
	        break;  
	      case 9: 
	      
	        task_asked ="T_filling_AQ_BU3";	
	        break;
	         
	      case 0: 
	        task_asked ="T_emptying_AQ"	;
	        break;     
	
	      }

  		}	
  }
  void Print_visual(String S){
  
  fill(0,0,0);
  noStroke();
  rect(share_visual_x*width,0,(float) (1-share_visual_x)*width,(float) 1*height );
  fill(255,255,255);
  text(S, (share_visual_x+(1-share_visual_x)*0.2)*width, (float) (height/2));
  
  }
  public void msg_received(String uneString){

    String[] S = split(uneString,"_");
   
   //Info sur etat d'une pompe : du type "P_M1-BR1_ON" 
    if (S[0].equals("P")){
    	get_pompe(S[0]+"_"+S[1]).set_state(S[2].equals("ON"));
    }
    
    //Demande d'info sur une electrode : 
    else if (S[0].equals("EL")){
    	
    }
    //Demande 
    else if (S[0].equals("ASK")){
    	//demande de tache
    	if(S[1].equals("T")){
    		//Envoyer 
    		myPort.write(task_asked + "\n");
    		task_asked = "null";
   		}
   		//demande de continuer 
    	if(S[1].equals("K")){
    		//Envoyer 
    		myPort.write("OK" + "\n");
    	}
    }
    else if (S[0].equals("T")){
    	//Tache debutée
    	if(S[1].equals("B")){
    		//Tache en cours 
    		task_executed = uneString;
    		//Revoyer OK
    		myPort.write("OK" + "\n"); 
   		}
   		//tache finie
   		if(S[1].equals("E")){
    		task_executed = "null";
    		//Revoyer OK
    		myPort.write("OK" + "\n"); 
   		}
   		
    }
   /* for (int j =0; j <les_pompes.length; j++ ){
      if (les_pompes[j].name.equals(S[0])){
        if (S[1].equals("ON")){
          les_pompes[j].set_state(true);
        }
        if (S[1].equals("OFF")){
          les_pompes[j].set_state(false);

        }

      }
    }*/
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
  
  
  public void mousePressed(){
      for (int i = 0 ; i<les_pompes.length; i++){
       // les_pompes[i].set_state(false);
        msg_received(les_pompes[i].name+"_OFF");
      }  
      //les_pompes[test].set_state(true);
     // System.out.println(les_pompes[test].name);
      msg_received(les_pompes[test].name+"_ON");
      Print_visual(les_pompes[test].name);
      test = (test +1)%14;
    }
    
    
 //Dessine tous les containers, les tuyaux et les pompes.    
  void dessiner(){
   //dessine les container 
    for (int i = 0 ; i<les_container.length; i++){
      les_container[i].dessiner();
    }
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


        break;
      case 2: 
        // Cas d'un bioreacteur 
        largeur = dimension_BR[0];
        hauteur = dimension_BR[1];
        volume=volume_BR;

        break;
      case 3: 
        // Cas d'un Buffer 
        largeur = dimension_BU[0];
        hauteur = dimension_BU[1];
        volume=volume_BU;



        break;
      case 4: 
        // Cas d'un aquarium 
        largeur = dimension_AQ[0];
        hauteur = dimension_AQ[1];
        volume=volume_AQ;

        break;
      case 5: 
        // Cas d'un stockage
        largeur = dimension_S[0];
        hauteur = dimension_S[1];
        volume=volume_S;
        break;

      }

    }


    void set_volume(float un_volume){
      volume_occ = un_volume;
    }
    void remplir(){
      float v = (float) ((temps*debit_pompe)/(60*volume));
      volume_occ =  volume_occ+ v;
    }
    void vider(){
      float v = (float) ((temps*debit_pompe)/(60*volume));
      volume_occ = volume_occ - v;
    }
    
    void dessiner(){
      //structure vide 
      stroke(0);
      fill(0,0,0);
      rect(Position[0]*width*share_visual_x,Position[1]*height*share_visual_y,width*share_visual_x*largeur,height*share_visual_y*hauteur);
      //structure remplie
      if (type == 1){
        fill(255,255,255);
      }
      else fill(0,255,0);
      rect(Position[0]*width*share_visual_x,Position[1]*height*share_visual_y+(height*share_visual_y*hauteur)*(1-volume_occ),width*share_visual_x*largeur,(height*share_visual_y*hauteur)*volume_occ);
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

      name = "P_"+container_pomp.name +"-"+container_refoul.name;
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

      name = "P"+container_pomp.name +"-"+container_refoul.name;
      
      

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



