import processing.serial.*;
import cc.arduino.*;

Arduino arduino;
//***** Pin des pompes *****\\
//pin 10 : P_BR_BU
//pin 11 : P_M1_BR1
//pin 12 : P_BU_AQ
//pin 13 : P_M2_BU

// /!\ Il faut installer la library arduino sous processing : Sketch -> Import library -> add Library - > 'chercher arduino' -> Arduino(firmata)

int P_BR_BU = 10;
int P_M1_BR1 = 11;
int P_BU_AQ = 12;
int P_M2_BU = 13;

void setup()
{
	//Pour choisir le bon port ou l'arduino est branché 
  println(Arduino.list());
  
  arduino = new Arduino(this, Arduino.list()[2 ], 57600);
  
  
	  //Declaration des pin comme output : 
    arduino.pinMode(P_BR_BU, Arduino.OUTPUT);
	arduino.pinMode(P_M1_BR1, Arduino.OUTPUT);
	arduino.pinMode(P_BU_AQ, Arduino.OUTPUT);
	arduino.pinMode(P_M2_BU, Arduino.OUTPUT);
	
  
}

void draw()
{
	//Test des pompes : 
	
  arduino.digitalWrite(P_BR_BU, arduino.HIGH);
  delay(1000);
  arduino.digitalWrite(P_BR_BU, arduino.LOW);
  arduino.digitalWrite(P_M1_BR1, arduino.HIGH);
  delay(1000);
  arduino.digitalWrite(P_M1_BR1, arduino.LOW);
  arduino.digitalWrite(P_BU_AQ, arduino.HIGH);
  delay(1000);
  arduino.digitalWrite(P_BU_AQ, arduino.LOW);
  arduino.digitalWrite(P_M2_BU, arduino.HIGH);
  delay(1000);
  arduino.digitalWrite(P_M2_BU, arduino.LOW);
  
  
  
  
}