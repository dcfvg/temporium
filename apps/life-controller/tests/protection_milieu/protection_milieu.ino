const int R = 10030;              // Résistance utilisée pour le montage pont diviseur de tension (en ohms)
const int V = 5;                  // Valeur de l'alimentation de l'Arduino, peu précis mais pas important pour le niveau de travail (en volts)

// pumps 
const int motorPinBioToAq = 6;    // bioreactor to aquarium ( fill with new alguae)
const int motorPinFoodToBio = 9;  // food to the bioreactor ( fill with new growing medium)
const int motorPinAqToTrash = 3;  // aquarium to trash      ( empty aquarium )
const int led = 13;

// sensors
const int bioreact_levelSensorPin = A0;    // bioreactor level sensor
const int aqua_levelSensorPin = A1;        // aquarium level sensor

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
boolean bioReactorFull = false;
boolean protectElectrod = false;

int protectElectrod_bioreactor[] = {motorPinBioToAq , motorPinAqToTrash};
int protectElectrod_aqua[] = {motorPinAqToTrash};

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
  Serial.print("bioReactorFull:" + String(bioReactorFull) + " \t " + "addAlguae:" + String(addAlguae)  + " \t " + "protectElectrod:" + String(protectElectrod) +"\n");
  monitor(100);
  
  // ORDERS ///////////////
  
  // alguae to aquarium     : start/stop
  addAlguae_ButtonState = digitalRead(addAlguae_ButtonPin);
  if (addAlguae_ButtonState && !addAlguae_prevButtonState){ // check previous button state and user action
    addAlguae = !addAlguae;  // toogle state
    Serial.print("addAlguae:" + String(addAlguae));
  }
  
  // empty aquarium         : start/stop
  emptyAqua_ButtonState = digitalRead(emptyAqua_ButtonPin);
  if (emptyAqua_ButtonState && !emptyAqua_prevButtonState){ // check previous button state and user action
    emptyAqua = !emptyAqua;  // toogle state
    Serial.print("emptyAqua:" + String(emptyAqua));
  }

  // ACTION ///////////////
  
  // add alguae to the aquarium
  if(addAlguae && bioReactorFull && !aquaFull()){
    digitalWrite(motorPinBioToAq, HIGH); 
    // Serial.println("La pompe PB2 fonctionne")
    bioReactorFull = true;
  }else{
    digitalWrite(motorPinBioToAq, LOW);
    if (addAlguae_ButtonState && !addAlguae_prevButtonState) bioReactorFull = false;
  }
  if(emptyAqua){
    digitalWrite(motorPinAqToTrash, HIGH);
  }else{
    digitalWrite(motorPinAqToTrash, LOW);
  }
  
  // add food 
  if(!bioReactorFull) fillBioReactor();
  
  // lower level to protect solution from electrod
  if (protectElectrod) electroProtection(protectElectrod_bioreactor);
  
  // keep previous state
  addAlguae_prevButtonState = addAlguae_ButtonState;
  emptyAqua_prevButtonState = emptyAqua_ButtonState;
  
  if(aquaFull) electroProtection(protectElectrod_aqua);
}
boolean aquaFull(){
  double V_mes = (analogRead(aqua_levelSensorPin)/1024.0)*5.0; //tension mesurée aux bornes de l'électrode
  double R_mes = (R*V_mes)/(V-V_mes); //mesure de la résistance de l'électrode
  
  if (R_mes > 200) { 
    return true;
  } else { 
    return false;
  }
}
void electroProtection(int motors[]){
  
  for (int i = 0; i<sizeof(motors); i++){
    digitalWrite(motors[i], HIGH);
  }

  Serial.print("On protège!!" + String(protectElectrod));
  
  //delay(5000);
  
  double V_mes = (analogRead(bioreact_levelSensorPin)/1024.0)*5.0; //tension mesurée aux bornes de l'électrode
  double R_mes = (R*V_mes)/(V-V_mes); //mesure de la résistance de l'électrode
  if (R_mes < 10){
    protectElectrod = false;
    for (int i = 0; i<sizeof(motors); i++){
      digitalWrite(motors[i], LOW);
    }
  }
    
  bioReactorFull = true;
  addAlguae = false;
}
void fillBioReactor(){
  double V_mes = (analogRead(bioreact_levelSensorPin)/1024.0)*5.0; //tension mesurée aux bornes de l'électrode
  double R_mes = (R*V_mes)/(V-V_mes); //mesure de la résistance de l'électrode

  Serial.print("V_mes = ");
  Serial.print(V_mes);
  Serial.print("\n R_mes = ");
  Serial.print(R_mes);

  if (R_mes < 2000){
    digitalWrite(motorPinFoodToBio, HIGH);
  }else{
    digitalWrite(motorPinFoodToBio, LOW);
    bioReactorFull = true;
    protectElectrod = true;
  }
}
void monitor(int speed){
  digitalWrite(led, LOW);        
  delay(speed);
  digitalWrite(led, HIGH);
}