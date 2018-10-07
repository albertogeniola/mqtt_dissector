from variable_headers import VariableHeader
from payloads import Payload
from fixed_headers import FixedHeader


class MQTTPacket(object):
    header = None  # type:FixedHeader
    vheader = None
    payload = None

    @staticmethod
    def parse(data):
        res = MQTTPacket()
        cursor = 0

        # Parse the fixed header. The fixed header is 2 bytes long
        res.header = FixedHeader.parse(data[cursor:])
        cursor += res.header.length

        # Parse the variable header.
        res.vheader = VariableHeader.parse(res.header, data[cursor:])
        cursor += res.vheader.length

        # Parse the payload
        res.payload = Payload.parse(res.header, res.vheader, data[cursor:])

        return res

    def __str__(self):
        return "================================\n" \
               "-----------FIXED HEADER---------\n" \
               "[Length]: %d bytes\n" \
               "%s\n" \
               "--------VARIABLE HEADER---------\n" \
               "[Length]: %d bytes\n" \
               "%s\n" \
               "------------PAYLOAD-------------\n" \
               "[Length]: %d bytes\n" \
               "%s\n" \
               "================================\n" % (self.header.length, str(self.header), self.vheader.length,  str(self.vheader), self.payload.length, str(self.payload))


if __name__ == '__main__':
    # Interpret the message as binary data
    data = [
        b'\x10\x7f\x00\x04MQTT\x04\xc2\x00\x1e\x008fmware:18050329735693251a0234298f1178ce_mKMqRrmMmf260000\x00\x1134:29:8f:11:78:ce\x00&46884_858d2e3a3a1aab502657d3a0473d95f3',
        b' \x02\x00\x00',
        b'\x82:\x00\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x01',
        b'\x90\x03\x00\x02\x01',
        b'2\xe7\x02\x003/appliance/18050329735693251a0234298f1178ce/publish\x00\x03{"header":{"messageId":"78f2c5ec4512ffd2a512380358423c8c","namespace":"Appliance.System.Clock","method":"PUSH","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":12,"timestampMs":630,"sign":"43b45082c309aafb9fe3a4cbaf05db1f"},"payload":{"clock":{"timestamp":12}}}',
        b'@\x02\x00\x03',
        b'2\xe9\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x00\x01{"header":{"messageId":"d7af48949d9f5a2ff4435a2e4ae5c212","namespace":"Appliance.System.Clock","timestamp":1537906364,"method":"PUSH","sign":"1edf975805ecadc13d1be73d6f640682","from":"/appliance/18050329735693251a0234298f1178ce/subscribe","payloadVersion":1},"payload":{"clock":{"timestamp":1537906365}}}',
        b'@\x02\x00\x01',
        b'2\xd0\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x00\x02{"header":{"messageId":"d8a3259264db70aa6d89e1cc3073c449","payloadVersion":1,"namespace":"Appliance.System.Debug","method":"GET","timestamp":1537906364,"from":"\\/cloud\\/18050329735693251a0234298f1178ce-9KSjs25M\\/subscribe","sign":"39661c33bbc545fd912a21c8494cdb68"},"payload":{}}',
        b'2\xcb\x07\x00:/cloud/18050329735693251a0234298f1178ce-9KSjs25M/subscribe\x00\x04{"header":{"messageId":"d8a3259264db70aa6d89e1cc3073c449","namespace":"Appliance.System.Debug","method":"GETACK","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906366,"timestampMs":580,"sign":"90653fd07e907869bb585996569cbac8"},"payload":{"debug":{"system":{"version":"1.1.15","compileTime":"2018-08-09 09:30:41","sysUpTime":"0h0m13s","memory":"Total 3322k, Free 1699k, Largest free block 1696k","suncalc":"5:13;17:15","localTime":"Tue Sep 25 20:12:46 2018","localTimeOffset":0},"network":{"linkStatus":0,"signal":73,"wifiDisconnectCount":0,"ssid":"MITM_WIFI","gatewayMac":"00:87:30:9a:0b:b5","innerIp":"192.168.10.88"},"cloud":{"activeServer":"iot.meross.com","mainServer":"iot.meross.com","mainPort":2001,"secondServer":"smart.meross.com","secondPort":2001,"userId":46884,"sysConnectTime":"N/A","sysOnlineTime":"N/A","sysDisconnectCount":0,"pingTrace":[]}}}}',
        b'@\x02\x00\x04',
        b'@\x02\x00\x02',
        b'2\xcd\t\x003/appliance/18050329735693251a0234298f1178ce/publish\x00\x05{"header":{"messageId":"f97a4bbf390407ed2cfb4be06f2c5a33","namespace":"Appliance.Control.Bind","method":"PUSH","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906369,"timestampMs":850,"sign":"214b28e779e6488d3bb8f90b7d22efbb"},"payload":{"bind":{"bindTime":1537906369,"time":{"timestamp":1537906369,"timezone":"Europe/Rome","timeRule":[[1521939600,7200,1],[1540688400,3600,0],[1553994000,7200,1],[1572138000,3600,0],[1585443600,7200,1],[1603587600,3600,0],[1616893200,7200,1],[1635642000,3600,0],[1648342800,7200,1],[1667091600,3600,0],[1679792400,7200,1],[1698541200,3600,0],[1711846800,7200,1],[1729990800,3600,0],[1743296400,7200,1],[1761440400,3600,0],[1774746000,7200,1],[1792890000,3600,0],[1806195600,7200,1],[1824944400,3600,0]]},"hardware":{"type":"mss310","subType":"us","version":"1.0.0","chipType":"MT7688","uuid":"18050329735693251a0234298f1178ce","macAddress":"34:29:8f:11:78:ce"},"firmware":{"version":"1.1.15","compileTime":"2018-08-09 09:30:41","wifiMac":"00:87:30:9a:0b:b5","innerIp":"192.168.10.88","server":"iot.meross.com","port":2001,"secondServer":"smart.meross.com","secondPort":2001,"userId":46884}}}}',
        b'@\x02\x00\x05',
        b'2\x90\x03\x003/appliance/18050329735693251a0234298f1178ce/publish\x00\x06{"header":{"messageId":"62b375e8d62e625cd653745eac41f452","namespace":"Appliance.System.Report","method":"PUSH","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906370,"timestampMs":0,"sign":"48daeaad7c913af7477445b501a6f972"},"payload":{"report":[{"type":"1","value":"0","timestamp":1537906370}]}}',
        b'@\x02\x00\x06',
        b'2\x81\x03\x003/appliance/18050329735693251a0234298f1178ce/publish\x00\x07{"header":{"messageId":"b843520e88c02f4a1d0372463301f662","namespace":"Appliance.Control.Toggle","method":"PUSH","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906370,"timestampMs":120,"sign":"f2ee9d987189a919687d673804b85680"},"payload":{"toggle":{"onoff":1,"lmTime":1537906368}}}',
        b'@\x02\x00\x07',
        b'2\xce\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x00\x03{"header":{"messageId":"8b5b26f74e272f31dbb646db44f9eeed","payloadVersion":1,"namespace":"Appliance.System.All","method":"GET","timestamp":1537906370,"from":"\\/cloud\\/18050329735693251a0234298f1178ce-G3TgJcdL\\/subscribe","sign":"f65729bb33af19a4868b8a02c6bb9289"},"payload":{}}',
        b'2\xab\n\x00:/cloud/18050329735693251a0234298f1178ce-G3TgJcdL/subscribe\x00\x08{"header":{"messageId":"8b5b26f74e272f31dbb646db44f9eeed","namespace":"Appliance.System.All","method":"GETACK","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906371,"timestampMs":110,"sign":"4211b2796028cbb91ff700f7bcd88a5a"},"payload":{"all":{"system":{"hardware":{"type":"mss310","subType":"us","version":"1.0.0","chipType":"MT7688","uuid":"18050329735693251a0234298f1178ce","macAddress":"34:29:8f:11:78:ce"},"firmware":{"version":"1.1.15","compileTime":"2018-08-09 09:30:41","wifiMac":"00:87:30:9a:0b:b5","innerIp":"192.168.10.88","server":"iot.meross.com","port":2001,"secondServer":"smart.meross.com","secondPort":2001,"userId":46884},"time":{"timestamp":1537906371,"timezone":"Europe/Rome","timeRule":[[1521939600,7200,1],[1540688400,3600,0],[1553994000,7200,1],[1572138000,3600,0],[1585443600,7200,1],[1603587600,3600,0],[1616893200,7200,1],[1635642000,3600,0],[1648342800,7200,1],[1667091600,3600,0],[1679792400,7200,1],[1698541200,3600,0],[1711846800,7200,1],[1729990800,3600,0],[1743296400,7200,1],[1761440400,3600,0],[1774746000,7200,1],[1792890000,3600,0],[1806195600,7200,1],[1824944400,3600,0]]},"online":{"status":1}},"control":{"toggle":{"onoff":1,"lmTime":1537906368},"trigger":[],"timer":[]}}}}',
        b'@\x02\x00\x08',
        b'2\xc6\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x00\x04{"header":{"from":"/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe","messageId":"c1085ab84832fcf6c30cafc643af5e7e","method":"GET","namespace":"Appliance.System.All","payloadVersion":1,"sign":"e2f768b444e1478b4aab4f3e11f88d43","timestamp":1537906369},"payload":{}}',
        b'2\xc6\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x00\x05{"header":{"from":"/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe","messageId":"e3606ee2eac5dce6949f1a127e15a66c","method":"GET","namespace":"Appliance.System.All","payloadVersion":1,"sign":"c849f9b7e1af3f1207c12cd4581e15da","timestamp":1537906370},"payload":{}}',
        b'2\xa6\n\x005/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe\x00\t{"header":{"messageId":"c1085ab84832fcf6c30cafc643af5e7e","namespace":"Appliance.System.All","method":"GETACK","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906371,"timestampMs":470,"sign":"6e6bed7d8c8798328b169341e01a3837"},"payload":{"all":{"system":{"hardware":{"type":"mss310","subType":"us","version":"1.0.0","chipType":"MT7688","uuid":"18050329735693251a0234298f1178ce","macAddress":"34:29:8f:11:78:ce"},"firmware":{"version":"1.1.15","compileTime":"2018-08-09 09:30:41","wifiMac":"00:87:30:9a:0b:b5","innerIp":"192.168.10.88","server":"iot.meross.com","port":2001,"secondServer":"smart.meross.com","secondPort":2001,"userId":46884},"time":{"timestamp":1537906371,"timezone":"Europe/Rome","timeRule":[[1521939600,7200,1],[1540688400,3600,0],[1553994000,7200,1],[1572138000,3600,0],[1585443600,7200,1],[1603587600,3600,0],[1616893200,7200,1],[1635642000,3600,0],[1648342800,7200,1],[1667091600,3600,0],[1679792400,7200,1],[1698541200,3600,0],[1711846800,7200,1],[1729990800,3600,0],[1743296400,7200,1],[1761440400,3600,0],[1774746000,7200,1],[1792890000,3600,0],[1806195600,7200,1],[1824944400,3600,0]]},"online":{"status":1}},"control":{"toggle":{"onoff":1,"lmTime":1537906368},"trigger":[],"timer":[]}}}}',
        b'@\x02\x00\t',
        b'2\xa6\n\x005/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe\x00\n{"header":{"messageId":"e3606ee2eac5dce6949f1a127e15a66c","namespace":"Appliance.System.All","method":"GETACK","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906371,"timestampMs":540,"sign":"8b366f20577cb1fbdebb780f6e060b03"},"payload":{"all":{"system":{"hardware":{"type":"mss310","subType":"us","version":"1.0.0","chipType":"MT7688","uuid":"18050329735693251a0234298f1178ce","macAddress":"34:29:8f:11:78:ce"},"firmware":{"version":"1.1.15","compileTime":"2018-08-09 09:30:41","wifiMac":"00:87:30:9a:0b:b5","innerIp":"192.168.10.88","server":"iot.meross.com","port":2001,"secondServer":"smart.meross.com","secondPort":2001,"userId":46884},"time":{"timestamp":1537906371,"timezone":"Europe/Rome","timeRule":[[1521939600,7200,1],[1540688400,3600,0],[1553994000,7200,1],[1572138000,3600,0],[1585443600,7200,1],[1603587600,3600,0],[1616893200,7200,1],[1635642000,3600,0],[1648342800,7200,1],[1667091600,3600,0],[1679792400,7200,1],[1698541200,3600,0],[1711846800,7200,1],[1729990800,3600,0],[1743296400,7200,1],[1761440400,3600,0],[1774746000,7200,1],[1792890000,3600,0],[1806195600,7200,1],[1824944400,3600,0]]},"online":{"status":1}},"control":{"toggle":{"onoff":1,"lmTime":1537906368},"trigger":[],"timer":[]}}}}',
        b'@\x02\x00\x05',
        b'2\xca\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x00\x06{"header":{"from":"/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe","messageId":"6dc1e441dc1866ae3db5d0c37dcf03bd","method":"GET","namespace":"Appliance.System.Ability","payloadVersion":1,"sign":"5f93ed19a6deb8b6f998819ec1bd8ffa","timestamp":1537906370},"payload":{}}',
        b'@\x02\x00\n',
        b'2\xc3\x08\x005/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe\x00\x0b{"header":{"messageId":"6dc1e441dc1866ae3db5d0c37dcf03bd","namespace":"Appliance.System.Ability","method":"GETACK","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906371,"timestampMs":680,"sign":"ba239a29858e7a8c67b5751204b4f1cd"},"payload":{"payloadVersion":1,"ability":{"Appliance.Config.Key":{},"Appliance.Config.WifiList":{},"Appliance.Config.Wifi":{},"Appliance.Config.Trace":{},"Appliance.System.Online":{},"Appliance.System.All":{},"Appliance.System.Hardware":{},"Appliance.System.Firmware":{},"Appliance.System.Time":{},"Appliance.System.Clock":{},"Appliance.System.Debug":{},"Appliance.System.Ability":{},"Appliance.System.Runtime":{},"Appliance.System.Report":{},"Appliance.System.Position":{},"Appliance.System.DNDMode":{},"Appliance.Control.Toggle":{},"Appliance.Control.Timer":{},"Appliance.Control.Trigger":{},"Appliance.Control.ConsumptionX":{},"Appliance.Control.Electricity":{},"Appliance.Control.Upgrade":{},"Appliance.Control.Bind":{},"Appliance.Control.Unbind":{}}}}',
        b'@\x02\x00\x06',
        b'2\xca\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x00\x07{"header":{"from":"/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe","messageId":"3df5708d395c401d04b133fe1c469f2a","method":"GET","namespace":"Appliance.System.Ability","payloadVersion":1,"sign":"21d8574fb4ce5678e3253f5ef6d20fd7","timestamp":1537906371},"payload":{}}',
        b'@\x02\x00\x0b',
        b'2\xc3\x08\x005/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe\x00\x0c{"header":{"messageId":"3df5708d395c401d04b133fe1c469f2a","namespace":"Appliance.System.Ability","method":"GETACK","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906371,"timestampMs":790,"sign":"21d8574fb4ce5678e3253f5ef6d20fd7"},"payload":{"payloadVersion":1,"ability":{"Appliance.Config.Key":{},"Appliance.Config.WifiList":{},"Appliance.Config.Wifi":{},"Appliance.Config.Trace":{},"Appliance.System.Online":{},"Appliance.System.All":{},"Appliance.System.Hardware":{},"Appliance.System.Firmware":{},"Appliance.System.Time":{},"Appliance.System.Clock":{},"Appliance.System.Debug":{},"Appliance.System.Ability":{},"Appliance.System.Runtime":{},"Appliance.System.Report":{},"Appliance.System.Position":{},"Appliance.System.DNDMode":{},"Appliance.Control.Toggle":{},"Appliance.Control.Timer":{},"Appliance.Control.Trigger":{},"Appliance.Control.ConsumptionX":{},"Appliance.Control.Electricity":{},"Appliance.Control.Upgrade":{},"Appliance.Control.Bind":{},"Appliance.Control.Unbind":{}}}}',
        b'@\x02\x00\x07',
        b'@\x02\x00\x0c',
        b'@\x02\x00\x04',
        b'2\xcb\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x00\x08{"header":{"from":"/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe","messageId":"f35ddb1678c736ce62bd5800c617de87","method":"GET","namespace":"Appliance.System.Position","payloadVersion":1,"sign":"aa2830433342fe82cafd4dfae9e2914d","timestamp":1537906371},"payload":{}}',
        b'2\xcb\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x00\t{"header":{"from":"/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe","messageId":"601d35ac3dc43ab0fcb806d2df76118e","method":"GET","namespace":"Appliance.System.Position","payloadVersion":1,"sign":"efc8560d10385c3600218845943767b8","timestamp":1537906371},"payload":{}}',
        b'2\x92\x03\x005/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe\x00\r{"header":{"messageId":"f35ddb1678c736ce62bd5800c617de87","namespace":"Appliance.System.Position","method":"GETACK","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906371,"timestampMs":970,"sign":"aa2830433342fe82cafd4dfae9e2914d"},"payload":{"position":{"longitude":9201235,"latitude":45511434}}}',
        b'@\x02\x00\r',
        b'2\x91\x03\x005/app/46884-7a33c0baa322f7c4cd38478ec599ee96/subscribe\x00\x0e{"header":{"messageId":"601d35ac3dc43ab0fcb806d2df76118e","namespace":"Appliance.System.Position","method":"GETACK","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":1537906372,"timestampMs":50,"sign":"f5788a43895bc1c44d12a31039fe14f1"},"payload":{"position":{"longitude":9201235,"latitude":45511434}}}',
        b'@\x02\x00\t',
        b'@\x02\x00\x0e',
        b'@\x02\x00\x08']

    for p in data:
        packet = MQTTPacket.parse(p)
        print(packet)

    # Missing:
    # At http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718039
    # From 3.8 SUBSCRIBE.

