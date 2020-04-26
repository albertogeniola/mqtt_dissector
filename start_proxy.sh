#!/bin/bash
mitmweb -p 8080 -m transparent --web-host 0.0.0.0 -s mitm_mqtt_addon.py --ssl-insecure --rawtcp
