const int R = 10030;              // Résistance utilisée pour le montage pont diviseur de tension (en ohms)
const int V = 5;                  // Valeur de l'alimentation de l'Arduino, peu précis mais pas important pour le niveau de travail (en volts)

// pumps 
const int motorPinBioToAq   = 6;    // bioreactor to aquarium ( fill with new alguae)
const int motorPinFoodToBio = 9;  // food to the bioreactor ( fill with new growing medium)
const int motorPinAqToTrash = 3;  // aquarium to trash      ( empty aquarium )
const int led = 13;

// electrodes
const int bioreact_levelSensorPin = A0;    // bioreactor level sensor
boolean   bioreact_protectElectrod = false;
int       bioreact_protectElectrodPumps[] = {motorPinBioToAq , motorPinAqToTrash};
boolean   bioreact_Full = false;

const int aqua_levelSensorPin = A2;        // aquarium level sensor
boolean   aqua_protectElectrod = false;
int       aqua_protectElectrodPumps[] = {motorPinAqToTrash};
boolean   aqua_Full = false;

// actions
boolean   addAlguae = false;
const int addAlguae_ButtonPin = 2;
boolean   addAlguae_prevButtonState = false;
int       addAlguae_ButtonState = 0;

boolean   emptyAqua = false;
const int emptyAqua_ButtonPin = 4;
boolean   emptyAqua_prevButtonState = false;
int       emptyAqua_ButtonState = 0;

// states

boolean debug = true;
boolean vFeedback = !debug; // [motorID 0-9][state 0-1]

void setup(){
  
  pinMode(bioreact_levelSensorPin, INPUT);
  
  pinMode(addAlguae_ButtonPin, INPUT);
  pinMode(emptyAqua_ButtonPin, INPUT);
  
  pinMode(motorPinBioToAq,OUTPUT);
  pinMode(motorPinFoodToBio,OUTPUT);
  pinMode(motorPinAqToTrash,OUTPUT);
  pinMode(led, OUTPUT);

  Serial.begin(9600);
}
void loop(){

  // debug
  if(debug) Serial.print("bioreact_Full:" + String(bioreact_Full) + " \t " + "addAlguae:" + String(addAlguae)  + " \t " + "aqua_Full:" + String(aqua_Full) +"\n");
  monitor(200);
  
  // ORDERS ///////////////
  //
  // alguae to aquarium     : start/stop
  addAlguae_ButtonState = digitalRead(addAlguae_ButtonPin);
  if (addAlguae_ButtonState && !addAlguae_prevButtonState){ // check previous button state and user action
    addAlguae = !addAlguae;  // toogle state
  }
  
  // empty aquarium         : start/stop
  emptyAqua_ButtonState = digitalRead(emptyAqua_ButtonPin);
  if (emptyAqua_ButtonState && !emptyAqua_prevButtonState){ // check previous button state and user action
    emptyAqua = !emptyAqua;  // toogle state
    if(debug) Serial.print("emptyAqua:" + String(emptyAqua));
  }

  // ACTION ///////////////
  //
  // add alguae to the aquarium
  
  if (is_full(bioreact_levelSensorPin)) addAlguae = false;
  
  if(addAlguae && is_full(bioreact_levelSensorPin)){
    digitalWrite(motorPinBioToAq, HIGH); 
    visual_feedback(motorPinBioToAq, 1);
    if(debug)Serial.println("bio -> aqua \t");
  }else{
    digitalWrite(motorPinBioToAq, LOW);
    visual_feedback(motorPinBioToAq, 0);
  }
  
  // empty aquarium
  if(emptyAqua){
    digitalWrite(motorPinAqToTrash, HIGH);
    visual_feedback(motorPinAqToTrash, 1);
    
    if(debug) Serial.println("aqua -> trash \t");
  }else{
    digitalWrite(motorPinAqToTrash, LOW);
    visual_feedback(motorPinAqToTrash, 0);
  }
  
  // fill BioReactor 
  if (!is_full(bioreact_levelSensorPin) && !addAlguae){
    
    digitalWrite(motorPinFoodToBio, HIGH);
    visual_feedback(motorPinFoodToBio, 1);
    
    if(debug)Serial.println("medium -> bioreact \t");
  }else{
    digitalWrite(motorPinFoodToBio, LOW);
    visual_feedback(motorPinFoodToBio, 0);
  }
  
  // keep previous state
  addAlguae_prevButtonState = addAlguae_ButtonState;
  emptyAqua_prevButtonState = emptyAqua_ButtonState;
  
  if(debug)Serial.print("\n");
}
boolean is_full(int sensorPin){
  double V_mes = (analogRead(sensorPin)/1024.0)*5.0; //tension mesurée aux bornes de l'électrode
  double R_mes = (R*V_mes)/(V-V_mes); //mesure de la résistance de l'électrode
  
  if (R_mes > 2000) { 
    return true;
  } else { 
    return false;
  }
}
void fillBioReactor(){
  if (!is_full(bioreact_levelSensorPin)){
    digitalWrite(motorPinFoodToBio, HIGH);
    visual_feedback(motorPinFoodToBio, 1);
    
    if(debug)Serial.println("medium -> bioreact \t");
  }else{
    digitalWrite(motorPinFoodToBio, LOW);
    visual_feedback(motorPinFoodToBio, 0);
  }
}
void monitor(int speed){  
  digitalWrite(led, LOW);        
  delay(speed);
  digitalWrite(led, HIGH);
}
void visual_feedback(int motor, int state){
  if(vFeedback){
    Serial.write((motor*10)+state);
  }
}