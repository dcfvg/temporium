int motorPin1 = 10;
int motorPin2 = 11;
int motorPin3 = 2;
int motorPin4 = 3;
int motorPin5 = 4;
int motorPin6 = 5;
int motorPin7 = 6;
int motorPin8 = 7;
int motorPin9 = 8;
int motorPin10 = 9;

void setup(){
  Serial.begin(9600);
  Serial.println("Hello World!");
  pinMode(motorPin1,OUTPUT);
  pinMode(motorPin2,OUTPUT);
  pinMode(motorPin3,OUTPUT);
  pinMode(motorPin4,OUTPUT);
  pinMode(motorPin5,OUTPUT);
  pinMode(motorPin6,OUTPUT);
  pinMode(motorPin7,OUTPUT);
  pinMode(motorPin8,OUTPUT);
  pinMode(motorPin9,OUTPUT);
  pinMode(motorPin10,OUTPUT);
}

void loop(){
  digitalWrite(motorPin1,HIGH);
  delay(1000);
  digitalWrite(motorPin1,LOW);
  digitalWrite(motorPin2,HIGH);
  delay(1000);
  digitalWrite(motorPin2,LOW);
  digitalWrite(motorPin3,HIGH);
  delay(1000);
  digitalWrite(motorPin3,LOW);
  digitalWrite(motorPin4,HIGH);
  delay(1000);
  digitalWrite(motorPin4,LOW);
  digitalWrite(motorPin5,HIGH);
  delay(1000);
  digitalWrite(motorPin5,LOW);
  digitalWrite(motorPin6,HIGH);
  delay(1000);
  digitalWrite(motorPin6,LOW);
  digitalWrite(motorPin7,HIGH);
  delay(1000);
  digitalWrite(motorPin7,LOW);
  digitalWrite(motorPin8,HIGH);
  delay(1000);
  digitalWrite(motorPin8,LOW);
  digitalWrite(motorPin9,HIGH);
  delay(1000);
  digitalWrite(motorPin9,LOW);
  digitalWrite(motorPin10,HIGH);
  delay(1000);
  digitalWrite(motorPin10,LOW);  
}