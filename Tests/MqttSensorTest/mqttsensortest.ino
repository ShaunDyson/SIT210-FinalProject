#include <string>
#include <cfloat>
#include "MQTT.h"
#include "Adafruit_DHT.h"

void callback(char* topic, byte* payload, unsigned length) {}

MQTT client("192.168.2.112", 1883, callback);
const auto dht_pin = D2;
const auto motion_pin = D8;
const auto dht_type = DHT22;
DHT dht{ dht_pin, dht_type };

const int read_interval = 2000;

void setup()
{
    pinMode(motion_pin, INPUT);
    dht.begin();
    client.connect("Argon");
}

void loop()
{
    if (client.isConnected())
    {
        const auto data = std::to_string(dht.getTempCelcius()) + "," + std::to_string(digitalRead(motion_pin) == HIGH);
        client.publish("SensingEvent", data.c_str());
        client.loop();
        delay(read_interval);
    }
}
