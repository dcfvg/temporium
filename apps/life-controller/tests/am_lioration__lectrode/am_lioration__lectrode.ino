const int levelSensorPin = A0;
const int levelButtonPin = 2;
const int motorPinA = 9;
const int motorPinB = 6;
const int motorPinC= 3;
const int led = 13;
const int R = 10030; // Résistance utilisée pour le montage pont diviseur de tension (en ohms)
const int V = 5; //Valeur de l'alimentation de l'Arduino, peu précis mais pas important pour le niveau de travail (en volts)

int buttonMemory = 0;
int levelElectrode = 0;


void setup(){
  pinMode(levelSensorPin, INPUT);
  pinMode(levelButtonPin, INPUT);
  pinMode(motorPinA,OUTPUT);
  pinMode(motorPinB,OUTPUT);
  pinMode(motorPinC,OUTPUT);
  pinMode(led, OUTPUT);
  Serial.begin(9600);
}

void loop(){ 

  digitalWrite(led, LOW);         // run monitor 
  int buttonsensorState = digitalRead(levelButtonPin);
  
  // ADD / maintaining level
  
  while (buttonsensorState==HIGH){
    digitalWrite(motorPinA, HIGH);
    buttonMemory = 1;
  }
 
  digitalWrite(motorPinA, LOW);
  
  while (buttonMemory==1 && buttonsensorState==LOW){
    
    double V_mes = (analogRead(levelSensorPin)/1024.0)*5.0; //tension mesurée aux bornes de l'électrode
    double R_mes = (R*V_mes)/(V-V_mes); //mesure de la résistance de l'électrode
  
    Serial.print("V_mes = ");
    Serial.print(V_mes);
    Serial.print("\n R_mes = ");
    Serial.print(R_mes);
    
    while (R_mes < 1  && buttonsensorState==LOW){
      digitalWrite(motorPinB, HIGH);
      //Serial.print(la pompe est allumée)
      levelElectrode = 1;
      
    }
    
    digitalWrite(motorPinB, LOW);
    
    if (levelElectrode == 1 && buttonsensorState==LOW){
      digitalWrite(motorPinA, HIGH);
      digitalWrite(motorPinC, HIGH);
      levelElectrode = 0;
      buttonMemory = 0;
      delay(5000);
     }
   }
 }


 
    
    
