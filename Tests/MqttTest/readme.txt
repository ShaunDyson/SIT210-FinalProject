The .ino file is for the Argon. The .py file is for the Raspberry Pi.

Before running this test, open the .ino file, find the line...
    MQTT client("192.168.2.112", 1883, callback);
and replace the IP Address with the IP Address of the Raspberry Pi.

You also need to include the MQTT library in the Particle App.
