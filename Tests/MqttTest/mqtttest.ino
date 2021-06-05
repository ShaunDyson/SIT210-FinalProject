#include <string>
#include "MQTT.h"

void callback(char* topic, byte* payload, unsigned int length) {}

int i = 0;
MQTT client("192.168.2.112", 1883, callback);

void setup()
{
    client.connect("Argon");
}

void loop()
{
    if (client.isConnected())
    {
        client.publish("TestEvent", std::to_string(i++).c_str());
        client.loop();
        delay(1000);
    }
}
