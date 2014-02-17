import processing.serial.*;


  int oldtime;
  int i ;

  container le_bioreacteur1;
  container le_bioreacteur2;
  container le_milieu1;
  container le_milieu2;
  container l_aquarium;
  container le_stockage;

  container les_container[];
  int test ; 
  
  Serial myPort;  // Create object from Serial class
  int inByte;

  //Position des elements 
  float[] position_bioreacteur1 ;
  float[] position_bioreacteur2;
  float[] position_milieu1; 
  float[] position_milieu2;
  float[] position_aquarium;
  float[] position_stockage;

  //Dimension des éléments: 

  float[] dimension_bioreacteur;
  float[] dimension_milieu; 
  float[] dimension_aquarium;
  float[] dimension_stockage;

  //Volume des container 
  float volume_bioreacteur ;
  float volume_milieu; 
  float volume_aquarium;
  float volume_stockage;
  //Pompes
  pompe[] les_pompes;
  float debit_pompe;
  
  String[] digit_pompe; //Nom des pompes dans l'ordre des pin digital

  float temps; //temps entre deux rafraichissement;

  int compteur;

  public void setup(){
    size(800,700);
    background(150);
    
    String portName = Serial.list()[2]; //change the 0 to a 1 or 2 etc. to match your port
myPort = new Serial(this, portName, 9600); 

    //On initilise les positions (de 0 à 1, en pourcentage de la taille de la fenetre): 

    position_milieu1 = new float[2];
    position_milieu1[0] = 0;
    position_milieu1[1] = 0;

    position_milieu2 = new float[2];
    position_milieu2[0] = (float) 0.5;
    position_milieu2[1] = (float) 0;

    position_bioreacteur1 = new float[2];
    position_bioreacteur1[0] =(float)  0.25;
    position_bioreacteur1[1] =(float)  (0.2+0.33*0.2);

    position_bioreacteur2 = new float[2];
    position_bioreacteur2[0] =(float)  0.5;
    position_bioreacteur2[1] = (float) (0.2+0.33*0.2);

    position_aquarium = new float[2];
    position_aquarium[0] = (float) 0.25;
    position_aquarium[1] = (float) (2*(0.2+0.33*0.2));

    position_stockage = new float [2];
    position_stockage[0] = (float) 0.5;
    position_stockage[1] =(float)  (3*(0.2+0.33*0.2));

    //On initialise les proportions (de 0 à 1 en pourcentage de la fenetre);

    dimension_milieu = new float[2];
    dimension_milieu[0] = (float) 0.3;
    dimension_milieu[1] = (float) 0.2;

    dimension_bioreacteur = new float[2];
    dimension_bioreacteur[0] =(float)  0.1;
    dimension_bioreacteur[1] =(float)  0.2;

    dimension_aquarium = new float[2];
    dimension_aquarium[0] = (float) 0.5;
    dimension_aquarium[1] = (float) 0.2;

    dimension_stockage = new float [2];
    dimension_stockage[0] = (float) 0.3;
    dimension_stockage[1] =(float)  0.2; 

    //Volume réel des trucs litre
    volume_bioreacteur =(float) 1.6  ;
    volume_milieu = (float) 10; 
    volume_aquarium =(float) 2.5;
    volume_stockage = (float) 1;

    les_pompes = new pompe[7];
    compteur=0;

    test = 0;

    //Instanciation des differents objets, avec bonne dimension :  

    les_container = new container[6];

    le_milieu1 = new container(position_milieu1,1,1,"le_milieu1");
    les_container[0] = le_milieu1;
    le_milieu2 = new container(position_milieu2,2,1,"le_milieu2");
    les_container[1] = le_milieu1;

    le_bioreacteur1 = new container(position_bioreacteur1,1,2,"le_bioreacteur1");
    les_container[2] = le_bioreacteur1;
    le_bioreacteur2 = new container(position_bioreacteur2,2,2,"le_bioreacteur2");
    les_container[3] = le_bioreacteur2;

    l_aquarium = new container(position_aquarium,1,3,"l_aquarium");
    les_container[4] = l_aquarium;
    le_stockage = new container(position_stockage,1,4,"le_stockage");
    les_container[5] = le_stockage;

    i = 0;

    //frequence de rafrichissement : 
    float frequence = 25;
    //frameRate(frequence);//rafraichissement une image toute les 40ms
    temps = (float) 1/frequence; 
    //Debit pompe : 
    debit_pompe = (float) 2;//en L/min
    le_milieu1.set_volume((float) (1));
    le_milieu2.set_volume((float) (1));

    le_bioreacteur1.set_volume((float) (i*0.01));
    le_bioreacteur1.set_concentration((float) (i*0.01));


    le_bioreacteur2.set_volume((float) (i*0.01));
    le_bioreacteur2.set_concentration((float) (i*0.01));


    l_aquarium.set_volume((float) (i*0.01));
    l_aquarium.set_concentration((float) (i*0.01));


    le_stockage.set_volume((float) (i*0.01));
    le_stockage.set_concentration((float) (i*0.01));

    for (int i = 0; i<6; i++){
      les_container[i].set_pompe();

    }
    for (int i = 0; i < 7; i++ ){
      System.out.println(les_pompes[i].name);
    }
    oldtime = 0;
    
    //Pompes branchees sur les Gigital pins , avec syntaxe PB1M1 pour pompe B1 -> M1
    digit_pompe = new String[14];
    digit_pompe[0] = "";
    digit_pompe[1] = "PM2B1";
    digit_pompe[2] = "PB1A";
    digit_pompe[3] = "";
    digit_pompe[4] = "";
    digit_pompe[5] = "";
    digit_pompe[6] = "";
    digit_pompe[7] = "";
    digit_pompe[8] = "";
    digit_pompe[9] = "";
    digit_pompe[10] ="";
    digit_pompe[11] ="";
    digit_pompe[12] ="PAS";
    digit_pompe[13] ="";

  }

  public void draw(){

    //on modifie les niveaux des different
    for (int j =0; j <7; j++ ){
      if (les_pompes[j].state){
        if (les_pompes[j].container_pomp.volume_occ>0 & les_pompes[j].container_refoul.volume_occ<1){
          les_pompes[j].container_pomp.vider();
          les_pompes[j].container_refoul.remplir();
        }

      }
    }
    
    if ( myPort.available() > 0) 
  {  
  inByte = myPort.read();  // read it and store it in val
  } 
 println(inByte);
 action_A(inByte);
  
    dessiner();
    
  }
  public void action_A(int N){
    int numero_digit_Pump = N/10; //Donne le numero du digital pin de la pompe
    int Pump_state = N % 10;
    String S = new String();
    S = digit_pompe[numero_digit_Pump];
    switch(Pump_state) {
    case 0: 
      S = S +"_OFF";
      break;
    case 1:
      S = S +"_ON";
      break;
    }
    println(S);
    action_Arduino(S);
  }
  public void action_Arduino(String uneString){
    
    String[] S = split(uneString,"_");

    for (int j =0; j <7; j++ ){
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
  /*public void mousePressed(){
    for (int i = 0 ; i<les_pompes.length; i++){
      les_pompes[i].set_state(false);
    }  
    les_pompes[test].set_state(true);
    System.out.println(les_pompes[test].name);
    test = (test +1)%7;
  }*/
  void dessiner(){
    le_milieu1.dessiner();
    le_milieu2.dessiner();
    le_bioreacteur1.dessiner();
    le_bioreacteur2.dessiner();
    l_aquarium.dessiner();
    le_stockage.dessiner();

    for (int i = 0 ; i<les_pompes.length; i++){
      les_pompes[i].dessiner_tuyau();
    }
    for (int i = 0 ; i<les_pompes.length; i++){
      if (!les_pompes[i].state) les_pompes[i].dessiner_pompe();
    }
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

    //Type de container : 1 Milieu de culture ; 2 Bioreacteur ; 3 Aquarium ; 4 stockage 
    int type;

    //Pompes 
    pompe[] pompes; //Nombre variable en fonction dy type 

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
        largeur = dimension_milieu[0];
        hauteur = dimension_milieu[1];
        volume=volume_milieu;


        break;
      case 2: 
        // Cas d'un bioreacteur 
        largeur = dimension_bioreacteur[0];
        hauteur = dimension_bioreacteur[1];
        volume=volume_bioreacteur;

        //On fabrique les pompes :


        pompes = new pompe[2];

        //Pompe entrée (Milieu de culture->bioreacteur)
        pompes[0] = new pompe( x,(float) (y - 0.2*0.165),1,Position, position_milieu2);
        les_pompes[compteur] = pompes[0];
        compteur = compteur + 1;

        //Pompe sortie (bioreacteur->Aquarium)
        pompes[1] = new pompe( x, (float) (y + hauteur + 0.2*0.165) ,1, Position, position_aquarium);
        les_pompes[compteur] = pompes[1];
        compteur = compteur + 1;

        break;
      case 3: 
        // Cas d'un aquarium 
        largeur = dimension_aquarium[0];
        hauteur = dimension_aquarium[1];
        volume=volume_aquarium;

        //On fabrique les pompes :

        pompes = new pompe[3];

        float[] Position_droite = new float[2];
        Position_droite[0] = (float) (P[0]+largeur);
        Position_droite[1] = P[1];

        //Pompe 1 = pompe pompe_filtrage;
        pompes[0] = new pompe( (float) (Position[0] + (largeur+0.1)),(float)(Position[1]-0.2*0.165),1,Position_droite,Position_droite);
        les_pompes[compteur] =pompes[0];
        compteur = compteur + 1;

        //Pompe 2 = pompe pompe_vidange (aquarium->stockage);
        pompes[1] = new pompe(  Position[0], (float) (Position[1]+(hauteur + 0.2*0.165)) ,1,Position,position_stockage);
        les_pompes[compteur] = pompes[1];
        compteur = compteur + 1;

        //Pompe 3 = pompe pompe_milieu_de (milieu-> aquarium )
        pompes[2] = new pompe( (float)(Position[0] - 0.1), (float)(Position[1]-0.2*0.165) ,1,Position,position_milieu1);
        les_pompes[compteur] = pompes[2];
        compteur = compteur + 1;


        break;
      case 4: 
        // Cas d'un stockage
        largeur = dimension_stockage[0];
        hauteur = dimension_stockage[1];
        volume=volume_stockage;
        break;

      }

    }

    void set_pompe(){
      switch(type) {
      case 1: 
        break;
      case 2: 

        //Pompe entrée (Milieu de culture->bioreacteur)
        pompes[0].set_pompe(le_milieu2,this);

        pompes[1].set_pompe( this, l_aquarium);


        break;
      case 3: 

        //Pompe 1 = filtrage
        pompes[0].set_pompe(this, this );
        //Pompe 2 = pompe pompe_vidange (aquarium->stockage);

        pompes[1].set_pompe(this,le_stockage );

        //Pompe 3 = pompe pompe_milieu_de (milieu-> aquarium )

        pompes[2].set_pompe(le_milieu1 , this);

        break;
      case 4: 
        // Cas d'un stockage
        largeur = dimension_stockage[0];
        hauteur = dimension_stockage[1];
        volume=volume_stockage;
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
      rect(Position[0]*width,Position[1]*height,width*largeur,height*hauteur);
      //structure remplie
      if (type == 1){
        fill(255,255,255);
      }
      else fill(0,255,0);
      rect(Position[0]*width,Position[1]*height+(height*hauteur)*(1-volume_occ),width*largeur,(height*hauteur)*volume_occ);


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
    float[] point_attache_1;
    float[] point_attache_2;

    //container 
    container container_pomp;//de pompage
    container container_refoul;//de refoulement


    //postion de la pompe : un_x, un_y 
    //P1 : postion du point d'accroche 1 
    //P2 postion du point d'accroche 2
    //pompe : container_1->container_2 
    pompe(float un_x, float un_y, int un_numero ,float[] P1,float[] P2){

      x = un_x;
      y = un_y; 
      le_numero = un_numero;
      state = false;

      point_attache_1 = P1;
      point_attache_2 = P2;


    }
    void set_pompe (container cont_1,container cont_2){
      //container 
      container_pomp = cont_1;//de pompage
      container_refoul = cont_2;//de refoulement

      if (container_pomp.name.equals("le_milieu1")){
        name = "PM1";
      }
      if (container_pomp.name.equals("le_milieu2")){
        name = "PM2";
      }
      if (container_pomp.name.equals("le_bioreacteur1")){
        name = "PB1";
      }
      if (container_pomp.name.equals("le_bioreacteur2")){
        name = "PB2";
      }
      if (container_pomp.name.equals("l_aquarium")){
        name = "PA";
      }
      if (container_pomp.name.equals("le_stockage")){
        name = "PS";
      }
      if (container_refoul.name.equals("le_milieu1")){
        name = name +"M1";
      }
      if (container_refoul.name.equals("le_milieu2")){
        name = name +"M2";
      }
      if (container_refoul.name.equals("le_bioreacteur1")){
        name = name + "B1";
      }
      if (container_refoul.name.equals("le_bioreacteur2")){
        name = name + "B2";
      }
      if (container_refoul.name.equals("l_aquarium")){
        name = name + "A";
      }
      if (container_refoul.name.equals("le_stockage")){
        name = name + "S";
      }

    }


    //dessine le chemin de la pompe
    void dessiner_tuyau(){
      if (state){
        stroke(0,255,0);
      }
      else stroke(0,0,0);

      strokeWeight(5);
      strokeCap(SQUARE);
      line(x*width,y*height, point_attache_1[0]*width, y*height);
      line(point_attache_1[0]*width,y*height, point_attache_1[0]*width, point_attache_1[1]*height);

      strokeWeight(5);
      strokeCap(SQUARE);
      line(x*width,y*height, point_attache_2[0]*width, y*height);
      line(point_attache_2[0]*width,y*height, point_attache_2[0]*width, point_attache_2[1]*height);


    }
    //On dessine la pompe
    void dessiner_pompe(){
      stroke(0);
      if (state){
        fill(0,255,0);
      }
      else fill(255,0,0);
      ellipse(x*width,y*height,width*largeur,height*hauteur);
    }
    void set_state(boolean B){
      state = B;
    }
  }



