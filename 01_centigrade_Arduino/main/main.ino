// Arduino NANO pinout
// 
// ---RFID RC522---
// 3V3 - 3.3V/VCC
// GND - GND
// D9  - RST(RESET)
// D10 - SDA(SS)
// D11 - MOSI
// D12 - MISO
// D13 - SCK 
// ----------------

// --MLX90614 DCI--
// 3V3 - VIN/VCC
// GND - GND
// A4  - SDA
// A5  - SCL
// ----------------

// ----HC-SR04----
// Gnd - GND
// Echo - D2
// Trig - D3
// Vcc - 5V
// ---------------

// for MLX
#include <Wire.h>
#include <Adafruit_MLX90614.h>

// for RFID
#include <SPI.h>
#include <MFRC522.h>

#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance. (RFID)

// variables for echo
long duration; 
int distance; 

// MLX object
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

double temp_amb;
double temp_obj;
double OUTLIER_TEMP_LOW = 30.0;
double OTLIER_TEMP_HIGH = 42.0;

int wait_miliseconds = 50;

String G_UID = "00000000";
String P_UID;

void setup() {
  Serial.begin(115200); 
  Serial.println("000");
  
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT

  mlx.begin(); //Initialize MLX90614

  SPI.begin();
  mfrc522.PCD_Init(); // init RFID
}

int loop_count = 0;

void loop() {  
  if (loop_count == 100){
    G_UID = "00000000";
    loop_count = 0;
  }
  read_uid();
  
  String data = "";
  data.concat(String(measure_distance()));
  data.concat("-");
  data.concat(String(get_avg_temp()));
  data.concat("-");
  data.concat(G_UID);
  Serial.println(data);
  
  delay(wait_miliseconds);
  loop_count++;
}
