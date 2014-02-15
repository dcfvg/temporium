
const int levelSensorPin = 2;
const int motorPinA = 9;
const int motorPinB = 6;
const int led = 13;

int sensorState = 0, timer = 0;
boolean pause = false, sec = true;

void setup(){
  pinMode(levelSensorPin, INPUT);
  pinMode(motorPinA,OUTPUT);
  pinMode(motorPinB,OUTPUT);
  pinMode(led, OUTPUT);
}

void loop(){ 

  digitalWrite(led, LOW);         // run monitor 
  
  // ADD / maintaining level
  
  sensorState = digitalRead(levelSensorPin);
  
  if (sensorState==LOW)digitalWrite(motorPinA, HIGH);
  else digitalWrite(motorPinA, LOW);

  // GET / random
  
  if(timer == 0) {
    timer = random(1 , 12) * 10; // random time
    pause = !pause;              // pause or pumping mode 
  }else{ 
    timer --;                    // count time
  }
  
  if (timer > 0 && ! pause) digitalWrite(motorPinB, HIGH); // pumping only if timer is not finished and not in pause
  else digitalWrite(motorPinB, LOW); 

  digitalWrite(led, HIGH);       // run monitor 
  delay(1000);                   // skectch resolution = 1s
}
