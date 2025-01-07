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

co2, moisture, soil_temp, luminance, aqi, aqi_value = None, None, None, None, None, None

import Line
def Msg_O(data:list):
    global co2, moisture, soil_temp, luminance, date, aqi, aqi_value
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

            case "AQI":
                aqi = data[0][1]
                print("aqi message:", aqi)
                
                aqi_value = int(aqi.split("️AQI指數：")[1].split(" (")[0])
                print("aqi value:", aqi_value) 
            
            case _: 
                print("data[0][0] is not in case.")

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
        # print("Line date:", date)

        # 構建發送給 LINE Notify 的消息
        m2_message = f"\nCO2: {co2} ppm, \nMoisture: {moisture}, \nSoil Temp: {soil_temp} °C, \nLuminance: {luminance} lux"
        # aqi_message = f"Date: {date}, \nAQI: {aqi}"
        
        aqi_message = ""

        if aqi != None:
            if aqi_value != None:
                if aqi_value >= 0 and aqi_value <= 50:
                    aqi_message = aqi + "\n\n" + "🌱建議措施: \n1️⃣正常進行農事活動，無需特殊處理。\n2️⃣定期檢查作物健康狀況，確保生長條件穩定。\n3️⃣持續監測空氣品質，以預防未來可能的污染。"
                elif aqi_value > 50 and aqi_value <= 100:
                    aqi_message = aqi + "\n\n" + "🌱建議措施: \n1️⃣注意觀察敏感作物（如豆類、番茄等）的葉片變化，防止早期損傷。\n2️⃣適當增加灌溉頻率，清洗植物表面的顆粒物。\n3️⃣考慮在高污染時間段（如中午）減少戶外農事操作。"
                elif aqi_value > 100 and aqi_value <= 150:
                    aqi_message = aqi + "\n\n" + "🌱建議措施: \n1️⃣為敏感作物提供遮陽網或臨時保護性結構，減少直接暴露於污染物中。\n2️⃣增加葉面肥噴灑，補充植物營養，提升抗性。\n3️⃣避免在污染高峰期進行施肥或農藥噴灑，防止與污染物產生化學反應。"
                elif aqi_value > 150 and aqi_value <= 200:
                    aqi_message = aqi + "\n\n" + "🌱建議措施: \n1️⃣加強植物表面清洗，防止污染物積累。\n2️⃣使用抗污染植物品種，減少高敏感作物的栽培。\n3️⃣停止修剪或其他可能引起植物傷口的操作，避免進一步損害。\n4️⃣增加溫室或遮罩結構的使用。"
                elif aqi_value > 200 and aqi_value <= 300:
                    aqi_message = aqi + "\n\n" + "🌱建議措施: \n1️⃣暫停所有戶外農事活動，避免污染物直接損害作物。\n2️⃣使用滴灌或微灌技術清除葉片和莖部的污染物。\n3️⃣在可能的情況下，提前採收成熟作物，減少損失。\n4️⃣避免種植高經濟價值但敏感的作物，改種耐污染品種。"
                else:
                    aqi_message = aqi + "\n\n" + "🌱建議措施: \n1️⃣將作物完全覆蓋或移入溫室（若條件允許）。\n2️⃣停止一切栽培活動，等待污染緩解。\n3️⃣進行土壤檢測，評估污染物沉積情況，必要時採取土壤修復措施。\n4️⃣評估農田長期影響，考慮輪作或休耕來恢復土壤和植物健康。"
            else:
                print("aqi_value is None")
        else:
            print("aqi is None")

        print("Line aqi:", aqi_message)

        soil_message = ""
        if(soil_temp != None):
            if(soil_temp < 20):
                soil_message = "\n🌡️溫度過低，請注意室內溫度"
            elif(soil_temp > 25):
                soil_message = "\n🌡️溫度過高，請注意室內溫度"
            else:
                soil_message = "\n🌡️目前為舒適溫度"
            
            print(soil_message)
        else:
            pass

        # 發送消息到 LINE Notify
        if (co2 != None and moisture != None and soil_temp != None and luminance != None and aqi != None and aqi_value != None):
            messages = m2_message + '\n' + soil_message + '\n\n' + aqi_message
            # messages = m2_message + '\n' + aqi_message + '\n' + soil_message + '\n' + aqi_message1
            Line.notify(messages)

        # 等待下一次更新
        time.sleep(exec_interval)  # 每隔一段時間抓取一次數據


