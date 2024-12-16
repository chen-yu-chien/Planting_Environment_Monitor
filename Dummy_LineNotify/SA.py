import uuid
import sys
import os
import time
import importlib.util

# 將 M2 資料夾加入 sys.path
sys.path.append(os.path.abspath('../M2'))

# 指定 M2/SA.py 的路徑
M2_module_path = os.path.abspath('../M2/SA.py')

# 動態載入 M2/SA.py
spec = importlib.util.spec_from_file_location("M2_SA", M2_module_path)
M2_SA = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M2_SA)


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

co2, moisture, soil_temp, luminance, date, aqi = None, None, None, None, None, None

import Line
def Msg_O(data:list):
    global co2, moisture, soil_temp, luminance, date, aqi
    # Line.notify(data[0])

    if type(data[0]) is list:
        match data[0][0]:
            case "co2":
                co2 = data[0][1]
                print("co2:", co2)

            case "luminance":
                luminance = data[0][1]
                print("luminance:", luminance)

            case "moisture":
                moisture = data[0][1]
                print("moisture:", moisture)

            case "soiltemp":
                soil_temp = data[0][1]
                print("soil_temp:", soil_temp)

            case _:
                date = data[0][0]
                aqi = data[0][1]
                print("date:", date, "aqi:", aqi)

    else:
        print("data[0] is not list")

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
        # co2_data = M2_SA.CO2()
        # moisture_data = M2_SA.Moisture()
        # soil_temp_data = M2_SA.SoilTemp()
        # luminance_data = M2_SA.Luminance_I()

        print("Line co2:", co2)
        print("Line moisture:", moisture)
        print("Line soil_temp:", soil_temp)
        print("Line luminance:", luminance)
        print("Line date:", date)
        print("Line aqi:", aqi)

        # 構建發送給 LINE Notify 的消息
        m2_message = f"\nCO2: {co2} ppm, \nMoisture: {moisture}, \nSoil Temp: {soil_temp} °C, \nLuminance: {luminance} lux"
        aqi_message = f"Date: {date}, \nAQI: {aqi}"
        
        soil_message = ""
        if(soil_temp != None):
            if(soil_temp < 20):
                soil_message = "溫度過低，請注意室內溫度"
                print("溫度過低，請注意室內溫度")
            elif(soil_temp > 25):
                soil_message = "溫度過高，請注意室內溫度"
                print("溫度過高，請注意室內溫度")
            else:
                soil_message = "目前為舒適溫度"
                print("目前為舒適溫度")
        else:
            pass

        lum_message = ""
        if(luminance != None):
            if(luminance > 65000):
                lum_message = "燈泡已關閉"
                print("燈泡已關閉")
            else:
                lum_message = "燈泡已開啟"
                print("燈泡已開啟")
        else:
            pass

        aqi_message1 = ""
        if(aqi != None):
            if(aqi <= 50):
                aqi_message1 = "空氣品質為良好，可正常戶外活動。"
            elif(aqi > 50 and aqi <= 100):
                aqi_message1 = "空氣品質普通，仍可正常戶外活動。"
            elif(aqi > 100 and aqi <= 150):
                aqi_message1 = "一般民眾如果有不適，應該考慮減少戶外活動。"
            elif(aqi > 150 and aqi <= 200):                     
                aqi_message1 = "一般民眾如果有不適，應減少體力消耗，特別是減少戶外活動。"
            elif(aqi > 200 and aqi <= 300):                     
                aqi_message1 = "所有人都可能產生較嚴重的健康影響，一般民眾應減少戶外活動。"
            else:
                aqi_message1 = "健康威脅達到緊急，一般民眾應避免戶外活動。"
        else:
            pass

        # 發送消息到 LINE Notify
        if (co2 != None and moisture != None and soil_temp != None and luminance != None and date != None 
            and aqi != None):
            messages = m2_message + '\n' + aqi_message + '\n' + soil_message + '\n' + lum_message + '\n' + aqi_message1
            Line.notify(messages)

        # 等待下一次更新
        time.sleep(exec_interval)  # 每隔一段時間抓取一次數據


