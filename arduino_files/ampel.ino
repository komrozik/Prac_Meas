// C++ code
//

int phase = 3*1000;
int current_time,old_time;
bool test;

void setup()
{
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  
  pinMode(5, INPUT);
  pinMode(6, INPUT);
  pinMode(7, INPUT);
  
  Serial.begin(9600);
  Serial.println("Rotphase");
  digitalWrite(2,HIGH);
  old_time = millis();
  test_volt();
}

void loop()
{	
  current_time = millis();
  if (digitalRead(5) && ! digitalRead(6) && ! digitalRead(7) && (current_time - old_time) >= phase)//Rotphase
  {
    Serial.println("Gelbphase");
    digitalWrite(2,HIGH);
    digitalWrite(3,HIGH);
    old_time = current_time;
    test_volt();
  }
  if (digitalRead(5) && digitalRead(6) && ! digitalRead(7) && (current_time - old_time) >= 1/3.*phase)//Gelbphase 1
  {
    Serial.println("Grünphase");
    digitalWrite(2,LOW);
    digitalWrite(3,LOW);
    digitalWrite(4,HIGH);
    old_time = current_time;
    test_volt();
  }
  if (! digitalRead(5) && ! digitalRead(6) && digitalRead(7) && (current_time - old_time) >= 2/3.*phase)//Grünphase
  {
    Serial.println("Gelbphase");
    digitalWrite(4,LOW);
    digitalWrite(3,HIGH);
    old_time = current_time;
    test_volt();
  }
  if (! digitalRead(5) && digitalRead(6) && ! digitalRead(7) && (current_time - old_time) >= 1/3.*phase)//Gelbphase 2
  {
    Serial.println("Rotphase");
    digitalWrite(3,LOW);
    digitalWrite(2,HIGH);
    old_time = current_time;
    test_volt();
  }
  if ((current_time - old_time) >= 3000){
    Serial.println("ERROR, Keine Ampelphase gefunden.");
    test_volt();
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
  Serial.print(digitalRead(5));
  Serial.print(" ,Ge ");
  Serial.print(digitalRead(6));
  Serial.print(" ,Gr ");
  Serial.print(digitalRead(7));
  Serial.print("\n");
  Serial.println("---------------");
}