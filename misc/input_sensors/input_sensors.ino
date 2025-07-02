//=============================//
//         SENSOR PINS        //
//=============================//
const int EC_sensor = A1;  
const int pH_sensor = A0;

const float temperature = 25.0;  
float kValue = 0.5;              

int rainwater_water_level_trig = 2,
    rainwater_water_level_echo = 3,
    fish_tank_water_level_trig = 4,
    fish_tank_water_level_echo = 5,
    ph_up_level_trig = 6,
    ph_up_level_echo = 7,
    ph_down_level_trig = 8,
    ph_down_level_echo = 9,
    fish_food_level_trig = 10,
    fish_food_level_echo = 11;

//=============================//
//     CONTAINER THRESHOLDS    //
//=============================//
float rainwater_cont_max = 200;
float rainwater_cont_min = 10;

float fish_cont_max = 100;
float fish_cont_min = 20; 

float ph_cont_max = 50;
float ph_cont_min = 10;

float fishfood_cont_max = 80;
float fishfood_cont_min = 10;

//=============================//
//            SETUP           //
//=============================//
void setup() {
  pinMode(rainwater_water_level_trig, OUTPUT);
  pinMode(rainwater_water_level_echo, INPUT);
  pinMode(fish_tank_water_level_trig, OUTPUT);
  pinMode(fish_tank_water_level_echo, INPUT);
  pinMode(ph_up_level_trig, OUTPUT);
  pinMode(ph_up_level_echo, INPUT);
  pinMode(ph_down_level_trig, OUTPUT);
  pinMode(ph_down_level_echo, INPUT);
  pinMode(fish_food_level_trig, OUTPUT);
  pinMode(fish_food_level_echo, INPUT);  

  Serial.begin(9600);
}

//=============================//
//             LOOP           //
//=============================//
void loop() {
  //=========== EC SENSOR GET DATA ===========//

  // https://wiki.dfrobot.com/Gravity__Analog_TDS_Sensor___Meter_For_Arduino_SKU__SEN0244
  // https://www.farnell.com/datasheets/4376692.pdf?utm_source
  int ec_raw = analogRead(EC_sensor); 
  float ec_voltage = ec_raw * (5.0 / 1024.0);
  float compensationCoefficient = 1.0 + 0.02 * (temperature - 25.0);

  // need references
  float ecRaw = (133.42 * ec_voltage * ec_voltage * ec_voltage) - (255.86 * ec_voltage * ec_voltage)  + (857.39 * ec_voltage);
  float uS_cm = ecRaw / compensationCoefficient;

  // https://www.snowate.com/knowledge-calculator/calculator/tds-ec-conversion.html
  float ppm = uS_cm * kValue * 0.55;

  // [23] https://www.landscape.sa.gov.au/mr/publications/measuring-salinity#:~:text=Conversion%20for%20units%20used%20to%20measure%20salinity:&text=Simply%20times%20(x)%20EC%20(,55.
  float ppt = ppm / 1000;

  //=========== PH SENSOR GET DATA ===========//
  float ph_raw = analogRead(pH_sensor);
  // 3.3 --> max voltage output of PH-4502C
  double ph_voltage = ph_raw * 3.3 / 1024;

  // https://raaflahar.medium.com/ph-4502c-sensor-diymore-how-to-use-and-calibrate-using-arduino-uno-r3-3afc2b96631
  // 2.5 --> reference for voltage at pH 7  
  // ph_voltage --> measured voltage 
  // 0.1841 --> voltage difference per pH unit 
  float pH = 7 + ((2.5 - ph_voltage) / 0.1841);
  //if (pH > 14.0) pH = 14.0;
  //if (pH < 0.0) pH = 0.0;

  //=========== LEVEL SENSORS ===========//
  float rainwater_level = get_distance_cm(rainwater_water_level_trig, rainwater_water_level_echo);
  float fish_tank_level = get_distance_cm(fish_tank_water_level_trig, fish_tank_water_level_echo);
  float ph_up_level = get_distance_cm(ph_up_level_trig, ph_up_level_echo);
  float ph_down_level = get_distance_cm(ph_down_level_trig, ph_down_level_echo);
  float fish_food_level = get_distance_cm(fish_food_level_trig, fish_food_level_echo);

  float cur_rwl   = get_current_level(rainwater_cont_max, rainwater_cont_min, rainwater_level);
  float cur_ftl   = get_current_level(fish_cont_max, fish_cont_min, fish_tank_level);
  float cur_phul  = get_current_level(ph_cont_max, ph_cont_min, ph_up_level);
  float cur_phdl  = get_current_level(ph_cont_max, ph_cont_min, ph_down_level);
  float cur_ffl   = get_current_level(fishfood_cont_max, fishfood_cont_min, fish_food_level);

  //=========== SERIAL PRINT ===========//
  Serial.print(pH); Serial.print(",");
  Serial.print(ppt); Serial.print(",");
  Serial.print(cur_rwl); Serial.print(",");
  Serial.print(cur_ftl); Serial.print(",");
  Serial.print(cur_phul); Serial.print(",");
  Serial.print(cur_phdl); Serial.print(",");
  Serial.println(cur_ffl);

  delay(1000);
}

//=============================//
//    ULTRASONIC MEASUREMENTS //
//=============================//
float get_distance_cm(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  float duration_us = pulseIn(echo, HIGH);
  float distance_cm = (duration_us * 0.0343) / 2;
  return distance_cm;
}

//=============================//
//   GET LEVEL IN PERCENTAGE  //
//=============================//
float get_current_level(float max_distance, float min_distance, float measured_distance) {
  float range = max_distance - min_distance;
  float filled = max_distance - measured_distance;
  float percentage = (filled / range) * 100.0;
  return constrain(percentage, 0.0, 100.0);
}
