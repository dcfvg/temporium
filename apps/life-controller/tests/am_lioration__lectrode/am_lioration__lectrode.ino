const int levelSensorPin = A0;
const int levelButtonPin = 2;
const int motorPinBioToAq = 6; // bioreactor to aquarium 
const int motorPinFoodToBio = 9; // food to the bioreactor
const int motorPinAqToTrash = 3; // aquarium to trash
const int led = 13;
const int R = 10030; // Résistance utilisée pour le montage pont diviseur de tension (en ohms)
const int V = 5; //Valeur de l'alimentation de l'Arduino, peu précis mais pas important pour le niveau de travail (en volts)
const int buttonMemory = 0;
const int levelElectrode = 0;

boolean addAlgue = false;
boolean bioReactorFull = false;
boolean prevButtonsensorState = false;
boolean electroProtect = false;
int buttonsensorState = 0;

void setup(){
  pinMode(levelSensorPin, INPUT);
  pinMode(levelButtonPin, INPUT);
  pinMode(motorPinBioToAq,OUTPUT);
  pinMode(motorPinFoodToBio,OUTPUT);
  pinMode(motorPinAqToTrash,OUTPUT);
  pinMode(led, OUTPUT);
  Serial.begin(9600);
}

void loop(){ 

  Serial.print("bioReactorFull:" + String(bioReactorFull) + " \t " + "addAlgue:" + String(addAlgue)  + " \t " + "electroProtect:" + String(electroProtect) +"\n");
 
  // run monitor 
  digitalWrite(led, LOW);        
  delay(100);
  digitalWrite(led, HIGH); 

  // check user action 
  buttonsensorState = digitalRead(levelButtonPin);
  if (buttonsensorState && !prevButtonsensorState){ // check previous button state to prevent double click
    addAlgue = !addAlgue;  // toogle state
    Serial.print("AddAlague" + String(addAlgue));
  }
  
  // add alguae to the aquarium
  if(addAlgue && bioReactorFull){
    digitalWrite(motorPinBioToAq, HIGH);
  }else{
    digitalWrite(motorPinBioToAq, LOW);
    bioReactorFull = false;
  }
  
  // add food 
  if(!bioReactorFull) {
    double V_mes = (analogRead(levelSensorPin)/1024.0)*5.0; //tension mesurée aux bornes de l'électrode
    double R_mes = (R*V_mes)/(V-V_mes); //mesure de la résistance de l'électrode

    Serial.print("V_mes = ");
    Serial.print(V_mes);
    Serial.print("\n R_mes = ");
    Serial.print(R_mes);

    if (R_mes < 1){
      digitalWrite(motorPinFoodToBio, HIGH);
    }else {
      digitalWrite(motorPinFoodToBio, LOW);
      bioReactorFull = true;
      electroProtect = true;
    }
  }
  // lower level to protect solution from electrod
  if (electroProtect){
    digitalWrite(motorPinBioToAq, HIGH);
    digitalWrite(motorPinAqToTrash, HIGH);
    
    delay(5000);
    
    digitalWrite(motorPinBioToAq, LOW);
    digitalWrite(motorPinAqToTrash, LOW);
    
    electroProtect = false;
    bioReactorFull = true;
    addAlgue = false;
  }
  prevButtonsensorState = buttonsensorState;
}







