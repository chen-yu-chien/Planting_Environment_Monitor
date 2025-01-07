import random
import time
import uuid
import crawl_weather_V8 as crawler 

ServerURL = 'https://class.iottalk.tw' #For example: 'https://DomainName'
MQTT_broker = 'iot.iottalk.tw' # MQTT Broker address, for example: 'DomainName' or None = no MQTT support
MQTT_port = 8883
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'Dummy_Device'
IDF_list = ['Dummy_Sensor']
# ODF_list = ['Dummy_Control']
device_id = str(uuid.uuid4()) #if None, device_id = MAC address
device_name = 'yc_aqi'
exec_interval = 10  # IDF/ODF interval

def Dummy_Sensor():
    crawler.data_crawling()
    if crawler.date_time != [] and crawler.aqi_value != []:
        position = "臺南市(臺南)"
        date_time = crawler.date_time[-1]
        aqi_value = crawler.aqi_value[-1]
        
        normal_alert = ""
        sensitive_alert = ""
        alert = ""

        if int(aqi_value) <= 50:
            aqi_value += " (良好)"
            normal_alert = "空氣品質良好，可以正常戶外活動。"
            sensitive_alert = "空氣品質良好，可以正常戶外活動。"

        elif 51 <= int(aqi_value) <= 100:
            aqi_value += " (普通)"
            normal_alert = "空氣品質普通，可以正常戶外活動。"
            sensitive_alert = "空氣品質普通，可能產生的咳嗽或呼吸急促症狀，但仍可正常戶外活動。"
        
        elif 101 <= int(aqi_value) <= 150:
            aqi_value += " (對敏感族群不健康)"
            normal_alert = "一般民眾仍可戶外運動，若有不適應該考慮減少戶外活動。學生建議減少長時間劇烈運動。"
            sensitive_alert = "建議減少體力消耗活動及戶外活動，必要外出應配戴口罩。具有氣喘的人可能需增加使用吸入劑的頻率。"
        
        elif 151 <= int(aqi_value) <= 200:
            aqi_value += " (對所有族群不健康)"
            normal_alert = "一般民眾如果有不適應減少體力消耗及戶外活動。學生應避免長時間劇烈運動，進行其他戶外活動時應增加休息時間。"
            sensitive_alert = "建議留在室內並減少體力消耗活動，必要外出應配戴口罩。具有氣喘的人可能需增加使用吸入劑的頻率。"
        
        elif 201 <= int(aqi_value) <= 300:
            aqi_value += " (非常不健康)"
            normal_alert = "一般民眾應減少戶外活動。學生應立即停止戶外活動，並將課程調整於室內進行。"
            sensitive_alert = "應留在室內並減少體力消耗活動，必要外出應配戴口罩。具有氣喘的人應增加使用吸入劑的頻率。"
        
        elif 301 <= int(aqi_value):
            aqi_value += " (危害)"
            normal_alert = "一般民眾應避免戶外活動，室內應緊閉門窗，必要外出應配戴口罩等防護用具。學生應立即停止戶外活動，並將課程調整於室內進行。"
            sensitive_alert = "應留在室內並避免體力消耗活動，必要外出應配戴口罩。具有氣喘的人應增加使用吸入劑的頻率。"

        alert = f"\n一般族群：{normal_alert}\n敏感族群：{sensitive_alert}"

        print("SA position:", position)
        print("SA date:", date_time)
        print("SA aqi:", aqi_value)
        print("SA alert", alert)

        message = f"📍地區：{position}\n🕒時間：{date_time}\n🌫️AQI指數：{aqi_value}\n💡提醒：{alert}"
        return message
    else:
        return None, None
    # return random.randint(0, 100), random.randint(0, 100) 

# def Dummy_Control(data:list):
#     print(data[0])

def on_register(r):
    print(f'Device name: {r["d_name"]}')

    # crawler.data_crawling()
    
    # # 等待下一次更新
    # time.sleep(exec_interval)  # 每隔一段時間抓取一次數據
    
    '''
    #You can write some SA routine code here, for example: 
    import time, DAI
    while True:
        DAI.push('Dummy_Sensor', [100, 200])  
        time.sleep(exec_interval)    
    '''


