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
        date_time = crawler.date_time[-1]
        aqi_value = crawler.aqi_value[-1]
        print("SA date:", date_time)
        print("SA aqi:", aqi_value)

        return date_time, float(aqi_value)
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


