const int levelSensorPin = 2;
const int motorPinA = 9;
const int motorPinB = 6;

int sensorState = 0, timer = 0;
boolean pause = false, sec = true;

void setup(){
  pinMode(levelSensorPin, INPUT);
  pinMode(motorPinA,OUTPUT);
  pinMode(motorPinB,OUTPUT);
}
void loop(){ 

  // IN / maintaining level
  sensorState = digitalRead(levelSensorPin);
  if (sensorState==LOW)digitalWrite(motorPinA, HIGH);
  else digitalWrite(motorPinA, LOW);

  // OUT / random 
  if(millis() % 1000 == 1 && sec){  // every seconds

    if(timer == 0) {
      timer = random(1 , 12) * 10; // random time
      pause = !pause;       // pause or pumping mode 
    }else{ 
      timer --;
    }

    if (timer > 0 && ! pause) digitalWrite(motorPinB, HIGH);
    else digitalWrite(motorPinB, LOW);
    sec = false;
  }else{
    sec = true;
  }
  delay(900);
}


