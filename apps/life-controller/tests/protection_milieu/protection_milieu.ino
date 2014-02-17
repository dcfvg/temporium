const int R = 10030;              // Résistance utilisée pour le montage pont diviseur de tension (en ohms)
const int V = 5;                  // Valeur de l'alimentation de l'Arduino, peu précis mais pas important pour le niveau de travail (en volts)
 
// pumps 
const int motorPinBioToAq   = 6;  // bioreactor to aquarium ( fill with new alguae)
const int motorPinFoodToBio = 9;  // food to the bioreactor ( fill with new growing medium)
const int motorPinAqToTrash = 3;  // aquarium to trash      ( empty aquarium )
const int led = 13;
 
// electrodes
const int bioreact_levelSensorPin = A3;    // bioreactor level sensor
boolean   bioreact_protectElectrod = false;
int       bioreact_protectElectrodPumps[] = { motorPinBioToAq , motorPinAqToTrash};
boolean   bioreact_Full = false;
boolean   bioreact_FullPrev = false;

const int aqua_levelSensorPin = A2;        // aquarium level sensor
boolean   aqua_protectElectrod = false;
int       aqua_protectElectrodPumps[] = {motorPinAqToTrash};
boolean   aqua_Full = false;
boolean   aqua_FullPrev = false;
 
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
 
boolean debug = false;
boolean vFeedback = !debug; // [motorID 0-9][state 0-1]
 
void setup(){
 
  pinMode(bioreact_levelSensorPin, INPUT);
  pinMode(aqua_levelSensorPin, INPUT);
 
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
  monitor(100);
 
  // ORDERS ///////////////
  //
  // alguae to aquarium     : start/stop
  addAlguae_ButtonState = digitalRead(addAlguae_ButtonPin);
  if(addAlguae_ButtonState && !addAlguae_prevButtonState){ // check previous button state and user action
    addAlguae = !addAlguae;  // toogle state
    if(debug) Serial.print("[press]addAlguae:" + String(addAlguae) + "\t");
  }
 
  // empty aquarium         : start/stop
  emptyAqua_ButtonState = digitalRead(emptyAqua_ButtonPin);
  if (emptyAqua_ButtonState && !emptyAqua_prevButtonState){ // check previous button state and user action
    emptyAqua = !emptyAqua;  // toogle state
    if(debug) Serial.print("[press]emptyAqua:" + String(emptyAqua) + "\t"); 
  }
 
  // ACTION ///////////////
  //
  // add alguae to the aquarium
   

  
  if(is_full(aqua_levelSensorPin)) addAlguae = false;
  
  if(addAlguae){ //  && is_full(bioreact_levelSensorPin) && !is_full(aqua_levelSensorPin)
 
    digitalWrite(motorPinBioToAq, HIGH);
    visual_feedback(motorPinBioToAq, 1);
 
    if(debug) Serial.println("bio -> aqua \t");
    bioreact_Full = true;
 
  }
  else{
    digitalWrite(motorPinBioToAq, LOW);
    visual_feedback(motorPinBioToAq, 0);
  }
 
  // empty aquarium
  if(emptyAqua){
    digitalWrite(motorPinAqToTrash, HIGH);
    visual_feedback(motorPinAqToTrash, 1);
 
    if(debug) Serial.println("aqua -> trash \t");
  }
  else{
    digitalWrite(motorPinAqToTrash, LOW);
    visual_feedback(motorPinAqToTrash, 0);
    if(debug) Serial.println("STOP aqua -> trash \t");
  }
 
  // fill BioReactor 
 
  if (!is_full(bioreact_levelSensorPin) && !addAlguae){
    digitalWrite(motorPinFoodToBio, HIGH);
    visual_feedback(motorPinFoodToBio, 1);
 
    if(debug)Serial.println("medium -> bioreact \t");
  }
  else{
    digitalWrite(motorPinFoodToBio, LOW);
    visual_feedback(motorPinFoodToBio, 0);
  }
  
  // send sensor visual feedback 
  if(bioreact_FullPrev != is_full(bioreact_levelSensorPin)) visual_feedback(3,is_full(bioreact_levelSensorPin) + 2);
  if(aqua_FullPrev != is_full(aqua_levelSensorPin)) visual_feedback(2,is_full(aqua_levelSensorPin) + 2);
  
  // keep previous state
  addAlguae_prevButtonState = addAlguae_ButtonState;
  emptyAqua_prevButtonState = emptyAqua_ButtonState;

  bioreact_FullPrev = is_full(bioreact_levelSensorPin);
  aqua_FullPrev = is_full(aqua_levelSensorPin);
  
  
  if(debug) Serial.println("\n");
}
boolean is_full(int sensorPin){
  double V_mes = (analogRead(sensorPin)/1024.0)*5.0; //tension mesurée aux bornes de l'électrode
  double R_mes = (R*V_mes)/(V-V_mes); //mesure de la résistance de l'électrode
 
  // Serial.print(String(sensorPin) + "V_mes = " );
  // Serial.print(V_mes);
  // Serial.print("R_mes = ");
  // Serial.print(R_mes);
  // Serial.print("\n"); 
 
  if (R_mes > 2000) { 
    return true;
  } 
  else { 
    return false;
  }
}
void monitor(int speed){  
  digitalWrite(led, LOW);        
  delay(speed);
  digitalWrite(led, HIGH);
}
void visual_feedback(int pin, int state){
  if(vFeedback){
    Serial.write((pin*10) + state);
  }
}
