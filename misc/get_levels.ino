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
    
//temp
float rainwater_cont_max = 200;
float rainwater_cont_min = 10;

float fish_cont_max = 100;
float fish_cont_min = 20; 

float ph_cont_max = 50;
float ph_cont_min = 10;

float fishfood_cont_max = 80;
float fishfood_cont_min = 10;

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

void loop() {
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

  Serial.print("Rainwater Level: "); Serial.print(cur_rwl); Serial.println(" %");
  Serial.print("Fish Tank Level: "); Serial.print(cur_ftl); Serial.println(" %");
  Serial.print("pH Up Level:     "); Serial.print(cur_phul); Serial.println(" %");
  Serial.print("pH Down Level:   "); Serial.print(cur_phdl); Serial.println(" %");
  Serial.print("Fish Food Level: "); Serial.print(cur_ffl); Serial.println(" %");
  Serial.println("------------------------------------------");

  delay(5000); 
}

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

float get_current_level(float max_distance, float min_distance, float measured_distance) {
  float range = max_distance - min_distance;
  float filled = max_distance - measured_distance;
  float percentage = (filled / range) * 100.0;
  return constrain(percentage, 0.0, 100.0);
}
