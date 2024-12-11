import random 

ServerURL = 'https://class.iottalk.tw' #For example: 'https://DomainName'
MQTT_broker = 'iot.iottalk.tw' # MQTT Broker address, for example: 'DomainName' or None = no MQTT support
MQTT_port = 8883 # Default port 1883(not encryption), 8883(encryption)
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'M2'
IDF_list = ['CO2', 'Luminance-I', 'Moisture', 'SoilTemp', 'pH']
# ODF_list = ['ODF313834004001','ODF313834004002']
import uuid
device_id = str(uuid.uuid4()) #if None, device_id = MAC address
device_name = 'yc_M2'
exec_interval = 1  # IDF/ODF interval

# def Dummy_Sensor():
#     return random.randint(0, 100), random.randint(0, 100) 

from sensors import sensorCO2_API
from sensors import sensorEC_API
from sensors import sensorPH_API
from sensors import sensorUV_API
# from sensors import sensorPS_API
# from sensors import sensorSHT31_API

ec = sensorEC_API()
ec.start()

ph = sensorPH_API()
ph.start()

uv = sensorUV_API()
uv.start()

co2 = sensorCO2_API()
co2.start()

# ps = sensorPS_API()
# ps.start()

# tp_and_rh = sensorSHT31_API()
# tp_and_rh.start()

def CO2():
    c = co2.getData()
    if c:  
        print('co2', float(c))
        return float(c)
    
def Luminance_I():
    _, l, _ = uv.getData()
    if l:  
        print('luminance', float(l))
        return float(l)
    
def Moisture():
    m, _, _ = ec.getData()
    if m:  
        print('moisture', float(m))
        return float(m)

def SoilTemp():
    _, st, _ = ec.getData()
    if st:  
        print('soiltemp', float(st))
        return float(st)

def pH():
    p = ph.getData()
    if p:  
        print('ph', float(p)) # no data
        return float(p)
    
def on_register(r):
    print(f'Device name: {r["d_name"]}')    
    '''
    #You can write some SA routine code here, for example: 
    import time, DAI
    while True:
        DAI.push('Dummy_Sensor', [100, 200])  
        time.sleep(exec_interval)    
    '''