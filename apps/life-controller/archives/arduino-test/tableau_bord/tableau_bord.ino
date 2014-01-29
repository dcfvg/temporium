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
  
  if(switchState == LOW){
    digitalWrite(3, LOW);
    digitalWrite(4, HIGH);
        delay(500);

    digitalWrite(5, LOW);
  }else{
    digitalWrite(3, HIGH);
    
    delay(1000);
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
  }
}

