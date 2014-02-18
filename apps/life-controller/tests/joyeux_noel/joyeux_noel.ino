//tableau de bord
  
int switchState = 0;
  
void setup(){
  pinMode(3,OUTPUT); 
  pinMode(4,OUTPUT); 
  pinMode(5,OUTPUT);
  pinMode(2,INPUT);   
}

void loop(){
  
  switchState = digitalRead(2);
  
  digitalWrite(random(2,6), HIGH);
  delay(random(0,200));
  digitalWrite(random(2,6), LOW);
  delay(random(0,200));
}

