#coding: utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

date_time = []
aqi_value = []

region = 'Tainan_AQI'
#台南測站觀測資料
url = 'https://airtw.moenv.gov.tw/'

def data_crawling():    
    #啟動模擬瀏覽器
    driver = webdriver.Chrome()

    #取得網頁代碼
    driver.get(url)
    open(region+'.html','wb').write(driver.page_source.encode('utf-8'))

    # 等待特定元素出現，例如 id 為 'aqicircle' 的元素
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ddl_site')))
    except:
        print("目標元素未出現，請檢查網頁是否正常載入")

    # 使用 Select 操作
    dropdown = driver.find_element(By.ID, 'ddl_site')
    select = Select(dropdown)
    select.select_by_visible_text("臺南")

    #指定 lxml 作為解析器
    soup = BeautifulSoup(driver.page_source, features='lxml')

    # 取得發布時間
    p = soup.find('p',{'id':'county_time'})
    date_time.append(p.find('span').text)

    # <div id='aqicircle'> 取得最新品質數值
    div = soup.find('div',{'id':'aqicircle'})
    div_in = div.find('div')
    aqi_value.append(div_in.find('b').text)


    print('crawl date:', date_time)
    print('crawl aqi:', aqi_value)



    # # 使用datetime取得時間年分
    # year = str(datetime.datetime.now().year)

    # # #對list中的每一項 <tr>
    # for tr in trs:
    # #   取時間, <tr>內的<th>, <th>內為時間 月/日<br>時:分
    #     d = tr.th.text
    #     d = year + d
    # #   字串轉為datetime格式
    #     date.append(datetime.datetime.strptime(d, '%Y%m/%d %H:%M'))
    #     temp.append(tr.find('td',{'headers':'temp'}).text)
    #     w_img=tr.find('td',{'headers':'weather'}).find('img')
    #     if w_img: weather.append(w_img['title'])  
    #     else: weather.append('-')      
    #     wind_direction.append(tr.find('td',{'headers':'w-1'}).text)
    #     wind_speed.append(tr.find('td',{'headers':'w-2'}).text)
    #     gust_wind.append(tr.find('td',{'headers':'w-3'}).text)
    #     visible.append(tr.find('td',{'headers':'visible-1'}).text)
    #     hum.append(tr.find('td',{'headers':'hum'}).text)
    #     pre.append(tr.find('td',{'headers':'pre'}).text)
    #     rain.append(tr.find('td',{'headers':'rain'}).text)
    #     sunlight.append(tr.find('td',{'headers':'sunlight'}).text)

    # temp.append(trs[0].find('td',{'headers':'temp'}).text)
    # hum.append(trs[0].find('td',{'headers':'hum'}).text)
    # pre.append(trs[0].find('td',{'headers':'pre'}).text)

    #關閉模擬瀏覽器       
    driver.quit()


# ---------------------------------------------------------------
import pandas as pd

table = {
"發布時間":date_time,
"空氣品質指數":aqi_value
}

df = pd.DataFrame(table)
df = df.reset_index(drop=True)    
df.to_csv(( region + '.csv'), encoding = 'utf-8')