import uuid
# import sys
# import os
# import time

# # 將 M2 資料夾路徑加入到 sys.path
# current_dir = os.path.dirname(os.path.abspath(__file__))  # 當前文件夾
# m2_path = os.path.join(current_dir, "..", "M2")  # M2 資料夾的路徑
# sys.path.append(m2_path)

# # 從 M2.SA.py 中導入 CO2 函數
# from SA import CO2

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
exec_interval = 1  # IDF/ODF interval

import Line
def Msg_O(data:list):
    # Line.notify(data[0])
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

    # while True:
    #     co2_data = CO2()
    #     # ph_data = PH()
    #     moisture_data = Moisture()
    #     soil_temp_data = SoilTemp()
    #     luminance_data = Luminance_I()

    #     # 構建發送給 LINE Notify 的消息
    #     message = f"CO2: {co2_data} ppm, Moisture: {moisture_data}, Soil Temp: {soil_temp_data} °C, Luminance: {luminance_data} lux"
        
    #     # 發送消息到 LINE Notify
    #     Line.notify(message)
        
    #     # 等待下一次更新
    #     time.sleep(exec_interval)  # 每隔一段時間抓取一次數據


