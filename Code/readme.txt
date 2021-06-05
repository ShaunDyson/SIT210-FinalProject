Open the .ino file, find the line...
    MQTT client("192.168.2.112", 1883, callback);
and replace the IP Address with the IP Address of your Raspberry Pi. Aftwards,
flash the .ino file to the Argon

Open 'app.py' in the 'Application Module' folder and replace 'IFTTT_KEY_HERE'
with your IFTTT Webhook Key. To find this, log into your IFTTT account, go to
the address below and click Documentation in the top-right.
https://ifttt.com/maker_webhooks

The Python scripts in the 'Application Module' folder should be copied to the
Raspberry Pi. Run the GUI app by running 'app.py'; the other scripts are there
to help 'app.py' do its job.
