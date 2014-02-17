// ACTIONS

// culture to aquarium 
const int cultureToAqua_pin   = 6; 
const int cultureToAqua_ButtonPin = 2;

boolean   cultureToAqua = false;
boolean   cultureToAqua_prevButtonState = false;
int       cultureToAqua_ButtonState = 0;


// aquarium to trash
const int aquaToTrash_pin = 3;
const int aquaToTrash_ButtonPin = 4;

boolean   aquaToTrash = false;      
boolean   aquaToTrash_prevButtonState = false;
int       aquaToTrash_ButtonState = 0;


// growing medium to aquarium
const int mediumToAqua_pin = 11;
const int mediumToAqua_ButtonPin = 7;

boolean   mediumToAqua = false;
boolean   mediumToAqua_prevButtonState = false;
int       mediumToAqua_ButtonState = 0;


// medium to the bioreactor ( fill with new growing medium)
const int mediumToBioreact_pin_pin = 9;  

const int led = 13;

// SENSORS

// bioreactor level sensor
const int bioreact_levelSensorPin = A3;   

boolean   bioreact_Full = false;
boolean   bioreact_FullPrev = false;

// aquarium level sensor
const int aqua_levelSensorPin = A2;        

boolean   aqua_Full = false;
boolean   aqua_FullPrev = false;

// PARAM
const int R = 10030;              // Résistance utilisée pour le montage pont diviseur de tension (en ohms)
const int V = 5;                  // Valeur de l'alimentation de l'Arduino, peu précis mais pas important pour le niveau de travail (en volts)
boolean debug = false;
boolean vFeedback = !debug; // [motorID 0-9][state 0-1]
 
void setup(){
 
  // electrod 
  pinMode(bioreact_levelSensorPin , INPUT);
  pinMode(aqua_levelSensorPin , INPUT);
 
  // buttons
  pinMode(cultureToAqua_ButtonPin , INPUT);
  pinMode(aquaToTrash_ButtonPin , INPUT);
  pinMode(mediumToAqua_pin, INPUT);
 
  // pumps
  pinMode(cultureToAqua_pin,OUTPUT);
  pinMode(mediumToBioreact_pin,OUTPUT);
  pinMode(aquaToTrash_pin,OUTPUT);
  
  // feedback
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  
}
void loop(){
 
  // debug
  monitor(100);
 
  // ORDERS ///////////////
  //
  // alguae to aquarium     : start/stop
  cultureToAqua_ButtonState = digitalRead(cultureToAqua_ButtonPin);
  if(cultureToAqua_ButtonState && !cultureToAqua_prevButtonState) cultureToAqua = !cultureToAqua;  // toogle state
  
  // medium to aquarium     : start/stop
  mediumToAqua_ButtonState = digitalRead(mediumToAqua_ButtonPin);
  if(mediumToAqua_ButtonState && !mediumToAqua_prevButtonState) mediumToAqua = !mediumToAqua;  // toogle state
  
  // empty aquarium         : start/stop
  aquaToTrash_ButtonState = digitalRead(aquaToTrash_ButtonPin);
  if (aquaToTrash_ButtonState && !aquaToTrash_prevButtonState) aquaToTrash = !aquaToTrash;  // toogle state

 
  // ACTION ///////////////
  //
  // add alguae to the aquarium
  
  if(is_full(aqua_levelSensorPin)) cultureToAqua = false; // check if aqurium is not full
  
  activePump(cultureToAqua_pin , cultureToAqua);          // add culture to aquarium
  activePump(mediumToAqua_pin , mediumToAqua);            // add growing medium to aquarium
  activePump(aquaToTrash_pin , aquaToTrash);              // put aquarium to trash
  activePump(mediumToBioreact_pin , !is_full(bioreact_levelSensorPin) && !cultureToAqua); // fill BioReactor
  
  // send sensor visual feedback 
  if(bioreact_FullPrev != is_full(bioreact_levelSensorPin)) visual_feedback(3,is_full(bioreact_levelSensorPin) + 2);
  if(aqua_FullPrev != is_full(aqua_levelSensorPin))         visual_feedback(2,is_full(aqua_levelSensorPin) + 2);
  
  // keep previous state
  cultureToAqua_prevButtonState = cultureToAqua_ButtonState;
  aquaToTrash_prevButtonState   = aquaToTrash_ButtonState;
  bioreact_FullPrev             = is_full(bioreact_levelSensorPin);
  aqua_FullPrev                 = is_full(aqua_levelSensorPin);
}
boolean is_full(int sensorPin){
  // poll electrod
  
  double V_mes = (analogRead(sensorPin)/1024.0)*5.0; //tension mesurée aux bornes de l'électrode
  double R_mes = (R*V_mes)/(V-V_mes); //mesure de la résistance de l'électrode
 
  if(debug){
    Serial.print(String(sensorPin) + "V_mes = " );
    Serial.print(V_mes);
    Serial.print("R_mes = ");
    Serial.print(R_mes);
    Serial.print("\n"); 
  }
 
  if (R_mes > 2000) { 
    return true;
  } 
  else { 
    return false;
  }
}
void activePump(int pin, boolean condition){
  // start/stop pump depending on state(true/false)
  
  if(condition){
    digitalWrite(pin, HIGH);
    visual_feedback(pin, 1); 
  }else{
    digitalWrite(pin, LOW);
    visual_feedback(pin, 0);
  }
}

// dev tools and feedback tools
void monitor(int speed){
  // led blinking
  digitalWrite(led, LOW);        
  delay(speed);
  digitalWrite(led, HIGH);
}
void visual_feedback(int pin, int state){
  // send serial feedback to visual_feedback.pde
  if(vFeedback){
    Serial.write((pin*10) + state);
  }
}