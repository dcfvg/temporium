int i; 
void setup() 
{
//initialize serial communications at a 9600 baud rate
Serial.begin(9600);
i = 0;
}
void loop()
{
//send 'Hello, world!' over the serial port
if (i<100) Serial.write(121);
else Serial.write(120);
i = i+1;
//wait 100 milliseconds so we don't drive ourselves crazy
delay(100);
}
