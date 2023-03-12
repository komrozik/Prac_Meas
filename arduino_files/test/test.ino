// C++ code
//

int phase = 3*1000;
int red = 2;
int yel = 3;
int gre = 4;
int current_time,old_time;
bool test;

void setup()
{
  pinMode(red, OUTPUT);
  pinMode(yel, OUTPUT);
  pinMode(gre, OUTPUT);

  Serial.begin(9600);
  Serial.println("Rotphase");
  digitalWrite(red,HIGH);
  old_time = millis();
  test_volt();
}

void loop()
{	
  current_time = millis();
  if (digitalRead(red) && ! digitalRead(yel) && ! digitalRead(gre) && (current_time - old_time) >= phase)//Rotphase
  {
    Serial.println("Gelbphase");
    digitalWrite(red,HIGH);
    digitalWrite(yel,HIGH);
    old_time = current_time;
    test_volt();
  }
  if (digitalRead(red) && digitalRead(yel) && ! digitalRead(gre) && (current_time - old_time) >= 1/3.*phase)//Gelbphase 1
  {
    Serial.println("Grünphase");
    digitalWrite(red,LOW);
    digitalWrite(yel,LOW);
    digitalWrite(gre,HIGH);
    old_time = current_time;
    test_volt();
  }
  if (! digitalRead(red) && ! digitalRead(yel) && digitalRead(gre) && (current_time - old_time) >= 2/3.*phase)//Grünphase
  {
    Serial.println("Gelbphase");
    digitalWrite(gre,LOW);
    digitalWrite(yel,HIGH);
    old_time = current_time;
    test_volt();
  }
  if (! digitalRead(red) && digitalRead(yel) && ! digitalRead(gre) && (current_time - old_time) >= 1/3.*phase)//Gelbphase 2
  {
    Serial.println("Rotphase");
    digitalWrite(yel,LOW);
    digitalWrite(red,HIGH);
    old_time = current_time;
    test_volt();
  }
  if ((current_time - old_time) >= 3000){
    Serial.println("ERROR, Keine Ampelphase gefunden.");
    Serial.print("Time: ");
  	Serial.print(old_time);
  	Serial.print(",Status Read: R");
  	Serial.print(digitalRead(red));
  	Serial.print(" ,Ge");
  	Serial.print(digitalRead(yel));
  	Serial.print(" ,Gr");
  	Serial.print(digitalRead(gre));
  	Serial.print("\n");
  }
}

void test_volt(){
  Serial.println("TEST:");
  Serial.print("old Time: ");
  Serial.print(old_time);
  Serial.print(",curr Time: ");
  Serial.print(current_time);
  Serial.print(",difference: ");
  Serial.print(current_time - old_time);
  Serial.print(",Status Read: R ");
  Serial.print(digitalRead(red));
  Serial.print(" ,Ge ");
  Serial.print(digitalRead(yel));
  Serial.print(" ,Gr ");
  Serial.print(digitalRead(gre));
  Serial.print("\n");
  Serial.println("---------------");
}