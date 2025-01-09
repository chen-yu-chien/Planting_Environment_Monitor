import random
import time
import uuid
from LineBot import add_co2, add_luminance, add_moisture, add_soil_temp, add_aqi, init
ServerURL = 'https://class.iottalk.tw' #For example: 'https://DomainName'
MQTT_broker = 'iot.iottalk.tw' # MQTT Broker address, for example: 'DomainName' or None = no MQTT support
MQTT_port = 8883
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'LineBot_process_data'
# IDF_list = ['Dummy_Sensor']
ODF_list = ['Msg-O']
device_id = str(uuid.uuid4()) #if None, device_id = MAC address
device_name = "yc_bot"
exec_interval = 10  # IDF/ODF interval

# co2, moisture, soil_temp, luminance, aqi, aqi_value = None, None, None, None, None, None
weather_info = []
message = None

def Msg_O(data:list):
    # global co2, moisture, soil_temp, luminance, aqi, aqi_value
    if type(data[0]) is list:
        weather_info.append(data[0])
        
        print("co2:", weather_info[-1][0])
        print("luminance:", weather_info[-1][1])
        print("moisture:", weather_info[-1][2])
        print("soil_temp:", weather_info[-1][3])
        
        aqi = weather_info[-1][4]
        aqi_value = int(aqi.split("️AQI指數：")[1].split(" (")[0])
        
        print("aqi message:", aqi)
        print("aqi value:", aqi_value)

        add_co2(float(weather_info[-1][0]))
        add_luminance(float(weather_info[-1][1]))
        add_moisture(float(weather_info[-1][2]))
        add_soil_temp(float(weather_info[-1][3]))        
        add_aqi(aqi, int(aqi_value))
        
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
    init()