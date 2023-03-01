
unsigned long V1;
void setup()
{
  pinMode(2, OUTPUT);
  Serial.begin(9600);
  digitalWrite(2,LOW);
}

void loop()
{
  V1 = millis()/1000;
  Serial.println("Zeit:");
  Serial.println(millis());
  if (V1%2){
    Serial.println("Turning LOW");
  	digitalWrite(2, LOW);
  }
  else{
    Serial.println("Turning HIGH");
    digitalWrite(2,HIGH);
  }
  delay(1000);
}