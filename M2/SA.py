import sys
import os
import uuid
import random
import time

sys.path.append(os.path.abspath('../Dummy_Device_IoTtalk_v1_py-master'))  # 添加 LineNotify_folder 到模組搜尋路徑
import Line  # 引入 LineNotify 模組 

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
# device_name = 'M2_final'
device_name = 'yc_M2'
exec_interval = 1  # IDF/ODF interval

# def Dummy_Sensor():
#     return random.randint(0, 100), random.randint(0, 100) 

from sensors import sensorCO2_API
# from sensors import sensorPH_API
from sensors import sensorMT_API
from sensors import sensorST_API
from sensors import sensorLM_API

co2 = sensorCO2_API()
co2.start()

# ph = sensorPH_API()
# ph.start()

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
    
# def PH():
#     p = ph.getData()
#     if p is not None:
#         print(f"PH Sensor data: {p}")
#         return float(p)
#     else:
#         print("PH Sensor failed to get data.")
#         return None

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

# 每次感測器數據更新後，將其發送到 LINE Notify
def send_line_notify(message):
    Line.notify(message)

def on_register(r):
    print(f'Device name: {r["d_name"]}') 
    
    while True:
        co2_data = CO2()
        # ph_data = PH()
        moisture_data = Moisture()
        soil_temp_data = SoilTemp()
        luminance_data = Luminance_I()

        # 構建發送給 LINE Notify 的消息
        message = f"CO2: {co2_data} ppm, Moisture: {moisture_data}, Soil Temp: {soil_temp_data} °C, Luminance: {luminance_data} lux"
        
        # 發送消息到 LINE Notify
        send_line_notify(message)

        # 等待下一次更新
        time.sleep(exec_interval)  # 每隔一段時間抓取一次數據

    '''
    #You can write some SA routine code here, for example: 
    import time, DAI
    while True:
        DAI.push('Dummy_Sensor', [100, 200])  
        time.sleep(exec_interval)    
    '''
