import random
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime 

ServerURL = 'https://class.iottalk.tw' #For example: 'https://DomainName'
MQTT_broker = 'iot.iottalk.tw' # MQTT Broker address, for example: 'DomainName' or None = no MQTT support
MQTT_port = 8883 # Default port 1883(not encryption), 8883(encryption)
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'M2'
IDF_list = ['Temperature', 'Humidity', 'AtPressure']
# ODF_list = ['ODF313834004001','ODF313834004002']
import uuid
device_id = str(uuid.uuid4()) #if None, device_id = MAC address
device_name = 'yc_M2'
exec_interval = 1  # IDF/ODF interval

# def Dummy_Sensor():
#     return random.randint(0, 100), random.randint(0, 100) 

# from crawl_weather_V8 import temp, hum, pre
# from sensors import sensorEC_API
# from sensors import sensorPH_API
# from sensors import sensorPS_API
# from sensors import sensorUV_API
# from sensors import sensorSHT31_API

# ps = sensorPS_API()
# ps.start()

# co2 = sensorCO2_API()
# co2.start()

# tp_and_rh = sensorSHT31_API()
# tp_and_rh.start()

# ec = sensorEC_API()
# ec.start()

# ph = sensorPH_API()
# ph.start()

# uv = sensorUV_API()
# uv.start()

temp = []
hum = []
pre = []

region = 'Tainan'
#台南測站觀測資料
url = 'https://www.cwa.gov.tw/V8/C/W/OBS_Station.html?ID=46741'

#啟動模擬瀏覽器
driver = webdriver.Chrome()

#取得網頁代碼
driver.get(url)
open(region+'.html','wb').write(driver.page_source.encode('utf-8'))


#指定 lxml 作為解析器
soup = BeautifulSoup(driver.page_source, features='lxml')

# <tbody id='obstime'> 抓過去24小時資料
tbody = soup.find('tbody',{'id':'obstime'})

# <tbody>内所有<tr>標籤
trs = tbody.find_all('tr')

# 使用datetime取得時間年分
year = str(datetime.datetime.now().year)

tr = trs[0]
temp = trs[0].find('td',{'headers':'temp'}).text
hum = trs[0].find('td',{'headers':'hum'}).text
pre = trs[0].find('td',{'headers':'pre'}).text

#關閉模擬瀏覽器       
driver.quit()

def AtPressure():
    # p = ps.getData()
    p = pre
    if p: 
        # atp, _, _ = p
        # print('atp', float(atp))
        # return float(atp)
        print('atp', float(p))
        return float(p)

# def CO2():
#     c = co2.getData()
#     if c:  
#         print('co2', float(c))
#         return float(c)

def Humidity():
    # t = tp_and_rh.getData()
    h = hum
    if h:  
        # tp, rh = t
        # print('rh', float(rh))
        # return float(rh)
        print('rh', float(h))
        return float(h)

def Temperature():
    # t = tp_and_rh.getData()
    t = temp
    if t:  
        # tp, rh = t
        # print('tp', float(tp))
        # return float(tp)
        print('tp', float(t))
        return float(t)

def on_register(r):
    print(f'Device name: {r["d_name"]}')    
    '''
    #You can write some SA routine code here, for example: 
    import time, DAI
    while True:
        DAI.push('Dummy_Sensor', [100, 200])  
        time.sleep(exec_interval)    
    '''