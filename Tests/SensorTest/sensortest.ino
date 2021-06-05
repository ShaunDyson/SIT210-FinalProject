#include <string>
#include <cfloat>
#include "Adafruit_DHT.h"

const auto dht_pin = D2;
const auto motion_pin = D8;
const auto dht_type = DHT22;
DHT dht{ dht_pin, dht_type };

const int read_interval = 2000;

void setup()
{
    pinMode(motion_pin, INPUT);
    dht.begin();
    Serial.begin(9600);
}

void loop()
{
    const auto temp = std::to_string(dht.getTempCelcius());
    const auto motion =  std::to_string(digitalRead(motion_pin) == HIGH);
    const auto data = "Temp: " + temp + ", Motion: " + motion;
    Serial.printlnf(data.c_str());
    delay(read_interval);
}