#!/bin/bash
mitmweb -p 8080 -m transparent --web-host 0.0.0.0 -s /home/webking/PycharmProjects/mqtt_dissector/mitm_mqtt_addon.py --ssl-insecure --rawtcp
#mitmweb -p 8080 -m transparent --web-host 0.0.0.0 -s ./mqtt_message.py --ssl-insecure --rawtcp
