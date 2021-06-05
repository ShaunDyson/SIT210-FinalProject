#include <string>
#include <cfloat>
#include "MQTT.h"
#include "Adafruit_DHT.h"

void callback(char* topic, byte* payload, unsigned length) {}

const auto dht_pin = D2;
const auto motion_pin = D8;
const auto dht_type = DHT22;
float temp = FLT_MIN;
MQTT client("192.168.2.112", 1883, callback);
DHT dht{ dht_pin, dht_type };

// temperature sensor occaisonally outputs 0. If it does it continuously
// though, it may mean it has become disconnected
int consecutive_temp_errors = 0;
// number of errors to tolerate before notifying application module
const int max_consecutive_temp_errors = 10;

const int read_interval = 2000;

 // update at least once a minute, regardless of if anything has changed.
 // If Application Module doesn't recieve an update at least once per minute,
 // it knows there's there's a connection issue.
const int update_interval = 60000;
int update_timer = 0;

void setup()
{
    pinMode(motion_pin, INPUT);
    dht.begin();
}

constexpr bool temp_is_error(const int temp_val)
{
    return temp_val < 1.0;
}

bool update_temperature()
{
    float new_temp = dht.getTempCelcius();

    // temperature sensor sometimes outputs erroneous 0s
    if (temp_is_error(new_temp))
    {
        consecutive_temp_errors++;
        return false;
    }

    consecutive_temp_errors = 0;

    // record temperature with single decimal point because minor
    // changes don't need to be sent to the Application Module
    new_temp *= 10;
    new_temp = int(new_temp) / 10.0;
    const bool changed = new_temp != temp;
    temp = new_temp;
    return changed;
}

bool detect_motion()
{
    return digitalRead(motion_pin) == HIGH;
}

void publish_events(const bool temp_changed, const bool motion)
{
    // to prevent unnecessary network traffic, only send update if
    // something has changed, or if it's time for a mandatory update.
    if (motion || temp_changed || update_timer <= 0)
    {
        const auto temp_str = temp_is_error(temp) ? "" : std::to_string(temp);
        const auto data = temp_str + "," + std::to_string(motion);
        client.publish("SensingEvent", data.c_str());
        update_timer = update_interval;
    }

    static bool error_published = false;
    const bool excessive_temp_errors = consecutive_temp_errors >= max_consecutive_temp_errors;

    if (excessive_temp_errors && !error_published)
    {
        error_published = true;
        client.publish("TempError", "Temperature Sensor may have become disconnected");
    }
    else if (!excessive_temp_errors && error_published)
    {
        error_published = false;
        client.publish("TempErrorClear", "Temperature Sensor is connected");
    }
}

void loop()
{
    if (client.isConnected())
    {
        publish_events(update_temperature(), detect_motion());
        update_timer -= read_interval;
        client.loop();
        delay(read_interval);
    }
    else // attempt to connect every 10 seconds
    {
        update_timer = 0; // update app as soon as connection is established
        client.connect("Argon");
        delay(10000);
    }
}
