/************
 * Author: Konstantin Mrozik
 * eMail: konstantin.mrozik@studium.uni-hamburg.de 
 * Date: 2023-03-01
 * 
 * This script reads a temperature
 * ****************/

#include <SD.h>
#include <SPI.h>
#include <RTClib.h>
#include <OneWire.h>
#include "temp_commands.h"

RTC_DS1307 rtc;

OneWire ow(4);

void setup()
{
  Serial.begin(9600);

  if(!rtc.begin()){
    Serial.println("RTC is NOT running. Let's set the time now!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  if(!SD.begin(10)){
    Serial.println("SD module initialization failed or SD Card is not present!");
    return;
  }

}

void loop()
{
  //Start 1st Sequence
  ow.reset();
  ow.write(CONVERT_T);
  
}