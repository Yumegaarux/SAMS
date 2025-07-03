const int EC_sensor = A1;  
const int pH_sensor = A0;

const float temperature = 25.0;  
float kValue = 0.5;              

void setup() {
  Serial.begin(9600); 
}

void loop() {
  // EC SENSOR GET DATA

  //https://wiki.dfrobot.com/Gravity__Analog_TDS_Sensor___Meter_For_Arduino_SKU__SEN0244
  //https://www.farnell.com/datasheets/4376692.pdf?utm_source
  int ec_raw = analogRead(EC_sensor); 
  float ec_voltage = ec_raw * (5.0 / 1024.0);
  float compensationCoefficient = 1.0 + 0.02 * (temperature - 25.0);

  //need references
  float ecRaw = (133.42 * ec_voltage * ec_voltage * ec_voltage) - (255.86 * ec_voltage * ec_voltage)  + (857.39 * ec_voltage);

  float uS_cm = ecRaw / compensationCoefficient;
  //https://www.snowate.com/knowledge-calculator/calculator/tds-ec-conversion.html
  float ppm = uS_cm * kValue * 0.55;
 
  //[23]  https://www.landscape.sa.gov.au/mr/publications/measuring-salinity#:~:text=Conversion%20for%20units%20used%20to%20measure%20salinity:&text=Simply%20times%20(x)%20EC%20(,55.
  float ppt = ppm / 1000;


  // PH LEVEL SENSOR GET DATA
  float ph_raw = analogRead(A0);
  // 3.3 --> max voltage output of PH-4502C
  double ph_voltage = ph_raw * 3.3 / 1024;

  // https://raaflahar.medium.com/ph-4502c-sensor-diymore-how-to-use-and-calibrate-using-arduino-uno-r3-3afc2b96631
  // 2.5 --> reference for voltage at pH 7  
  // ph_voltage --> measured voltage 
  // 0.1841 --> voltage difference per pH unit 
  float pH = 7+((2.5 - ph_voltage)/0.1841);

  //if (pH > 14.0) pH = 14.0;
  //if (pH < 0.0) pH = 0.0;

  Serial.print(pH);
  Serial.print(",");
  Serial.println(ppt);

  delay(1000);
}
