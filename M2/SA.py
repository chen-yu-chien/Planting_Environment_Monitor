import sys
import os
import uuid
import random
import time

ServerURL = 'https://class.iottalk.tw' #For example: 'https://DomainName'
MQTT_broker = 'iot.iottalk.tw' # MQTT Broker address, for example: 'DomainName' or None = no MQTT support
MQTT_port = 8883 # Default port 1883(not encryption), 8883(encryption)
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'M2'
IDF_list = ['CO2', 'Moisture', 'SoilTemp', 'Luminance-I']
# ODF_list = ['ODF313834004001','ODF313834004002']
import uuid
device_id = str(uuid.uuid4()) #if None, device_id = MAC address
device_name = 'yc_M2'
exec_interval = 1  # IDF/ODF interval

from sensors import sensorCO2_API
from sensors import sensorMT_API
from sensors import sensorST_API
from sensors import sensorLM_API

co2 = sensorCO2_API()
co2.start()

mt = sensorMT_API()
mt.start()

st = sensorST_API()
st.start()

lm = sensorLM_API()
lm.start()

def CO2():
    c = co2.getData()
    if c is not None:
        print(f"CO2 Sensor data: {c}")
        return float(c)
    else:
        print("CO2 Sensor failed to get data.")
        return None

def Moisture():
    m = mt.getData()
    if m is not None:
        print(f"Moisture Sensor data: {m}")
        return float(m)
    else:
        print("Moisture Sensor failed to get data.")
        return None

def SoilTemp():
    s = st.getData()
    if s is not None:
        print(f"Soil Temp Sensor data: {s}")
        return float(s)
    else:
        print("Soil Temp Sensor failed to get data.")
        return None
    
def Luminance_I():
    l = lm.getData()
    if l is not None:
        print(f"Luminance Sensor data: {l}")
        return float(l)
    else:
        print("Luminance Sensor failed to get data.")
        return None

def on_register(r):
    print(f'Device name: {r["d_name"]}') 
    '''
    #You can write some SA routine code here, for example: 
    import time, DAI
    while True:
        DAI.push('Dummy_Sensor', [100, 200])  
        time.sleep(exec_interval)    
    '''
