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

// User-defined constant
const String logfile = "tsensor.log";


RTC_DS1307 rtc;
OneWire ow(4);


void setup()
{
  Serial.begin(9600);

  if(!rtc.begin()){
    Serial.println("RTC is NOT running. Let's set the time now!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  /******
   * When the time needsd to be set on a new device, or after a power loss, the following line sets the RTC to the date & time this sketch was compiled(!)
  */
  // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  if(!SD.begin(10)){
    Serial.println("SD module initialization failed or SD Card is not present!");
    return;
  }

  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  
  save_header();

}

void loop()
{
  byte rom_code[8]; // create array with 8 bytes (64 bits)
  byte sp_data[9]; // Scratchpad data

  //Start sequence to read out the rom code
  ow.reset();
  ow.write(READ_ROM);
  for (int i = 0; i<8; i++) {
    rom_code[i] = ow.read();
  }
  if(rom_code[0] != IS_DS18B20_SENSOR){
    Serial.print("Sensor is not a DS18B20 sensor!");
    return;
  }
  String registration_number;
  for (int i = 1; i<7;i++){
    registration_number += String(rom_code[i], HEX);
  }
  
  // Start Sequence for converting temperatures

  ow.reset();
  ow.write(SKIP_ROM);
  ow.write(CONVERT_T);

  // Start sequence for reading data from scratchpad
  ow.reset();
  ow.write(SKIP_ROM);
  ow.write(READ_SCRATCH);
  for (int i = 0; i<9;i++){
    sp_data[i] = ow.read();
  }

  int16_t tempRead = sp_data[1] << 8 | sp_data[0];
  
  float tempCelsius = tempRead/16.;
  // LED(int(tempCelsius));
  String time_now= getISOtime();
  save_data_point(time_now,registration_number,tempCelsius);
  delay(1000);

}

void save_data_point(String time,String reg,float spot){//,float avg){
  printOutput(time);
  printOutput(", ");
  printOutput(String(millis()));
  printOutput(", ");
  printOutput(reg);
  printOutput(", ");
  printOutputln(String(spot));
  // printOutput(", ");
  // printOutputln(avg);
}

void save_header(){
  printOutput("# Date");
  printOutput(", ");
  printOutput("millis");
  printOutput(", ");
  printOutput("sensor_id");
  printOutput(", ");
  printOutputln("spot_meas");
  // printOutput(", ");
  // printOutputln("avg_meas");
}

void LED(int signal){
    if (signal < -20){
        digitalWrite(5,255);
        digitalWrite(6,0);
      }
      else if(signal > 40){
      digitalWrite(6,255);
        digitalWrite(5,0);
      }
      else if (signal > -20 && signal < 40){
        int brightness = ((signal + 20. )/60.)*255;
        analogWrite(5,255 - brightness);
        analogWrite(6,brightness);
      }
}