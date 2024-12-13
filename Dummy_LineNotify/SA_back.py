import uuid
import sys
import os
import time
import importlib.util

# 將 M2 資料夾加入 sys.path
sys.path.append(os.path.abspath('../M2'))
sys.path.append(os.path.abspath('../Dummy_AQISensor'))

# 指定 M2/SA.py 的路徑
M2_module_path = os.path.abspath('../M2/SA.py')
AQI_module_path = os.path.abspath('../Dummy_AQISensor/SA.py')

# 動態載入 M2/SA.py
spec = importlib.util.spec_from_file_location("M2_SA", M2_module_path)
M2_SA = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M2_SA)

# 動態載入 M2/SA.py
spec = importlib.util.spec_from_file_location("AQI_SA", AQI_module_path)
AQI_SA = importlib.util.module_from_spec(spec)
spec.loader.exec_module(AQI_SA)


ServerURL = 'https://class.iottalk.tw' #For example: 'https://DomainName'
MQTT_broker = 'iot.iottalk.tw' # MQTT Broker address, for example: 'DomainName' or None = no MQTT support
MQTT_port = 8883
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'LineNotify'
ODF_list = ['Msg-O']
device_id = str(uuid.uuid4()) #if None, device_id = MAC address
device_name = 'yc_Line'
exec_interval = 10  # IDF/ODF interval

date, aqi = "", ""

import Line
def Msg_O(data:list):
    global date, aqi
    # Line.notify(data[0])
    print(data[0], type(data[0]))

    if type(data[0]) is list:
        if len(data[0]) > 1:
            date = data[0][0]
            aqi = data[0][1]
            print(type(date), type(aqi))

def on_register(r):
    print(f'Device name: {r["d_name"]}')    
    '''
    #You can write some SA routine code here, for example: 
    import time, DAI
    while True:
        DAI.push('Dummy_Sensor', [100, 200])  
        time.sleep(exec_interval)    
    '''

    while True:
        co2_data = M2_SA.CO2()
        # ph_data = PH()
        moisture_data = M2_SA.Moisture()
        soil_temp_data = M2_SA.SoilTemp()
        luminance_data = M2_SA.Luminance_I()
        # date, aqi = AQI_SA.Dummy_Sensor()

        print("Line date:", date)
        print("Line aqi:", aqi)

        # 構建發送給 LINE Notify 的消息
        m2_message = f"CO2: {co2_data} ppm, Moisture: {moisture_data}, Soil Temp: {soil_temp_data} °C, Luminance: {luminance_data} lux"
        aqi_message = f"Date: {date}, AQI: {aqi}"
        
        # 發送消息到 LINE Notify
        if (co2_data != None and moisture_data != None and soil_temp_data != None and luminance_data != None and date != None 
            and aqi != None):
            messages = m2_message + '\n' + aqi_message
            Line.notify(messages)
        
        # 等待下一次更新
        time.sleep(exec_interval)  # 每隔一段時間抓取一次數據


