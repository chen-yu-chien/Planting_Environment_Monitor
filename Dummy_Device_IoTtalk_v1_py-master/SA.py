import uuid

ServerURL = 'https://class.iottalk.tw' #For example: 'https://DomainName'
MQTT_broker = 'iot.iottalk.tw' # MQTT Broker address, for example: 'DomainName' or None = no MQTT support
MQTT_port = 8883
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'LineNotify'
ODF_list = ['Msg-O']
device_id = str(uuid.uuid4()) #if None, device_id = MAC address
device_name = 'XiesLine'
exec_interval = 1  # IDF/ODF interval

import Line
def Msg_O(data:list):
    Line.notify(data[0])
    print(data[0])

def on_register(r):
    print(f'Device name: {r["d_name"]}')    
    '''
    #You can write some SA routine code here, for example: 
    import time, DAI
    while True:
        DAI.push('Dummy_Sensor', [100, 200])  
        time.sleep(exec_interval)    
    '''


