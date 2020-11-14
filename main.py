from mitmproxy.tools.main import mitmweb

#
if __name__ == '__main__':
    mitmweb(args=["-p", "8080", "--web-host", "0.0.0.0", "-s", "mitm_mqtt_addon.py", "-m", "transparent", "--rawtcp"])
