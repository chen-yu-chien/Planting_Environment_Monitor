# -*- coding: UTF-8 -*-
import time, threading
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import config

line_bot_api = LineBotApi(config.ChannelAccessToken) #LineBot's Channel access token
handler = WebhookHandler(config.ChannelSecret)       #LineBot's Channel secret
user_id_set=set()                                    #LineBot's Friend's user id 
app = Flask(__name__)

def loadUserId():
    try:
        idFile = open(config.idfilePath, 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None

def saveUserId(userId):
        idFile = open(config.idfilePath, 'a')
        idFile.write(userId+';')
        idFile.close()


def pushLineMsg(Msg):
    for userId in user_id_set:
        try:
            line_bot_api.push_message(userId, TextSendMessage(text=Msg))
        except Exception as e:
            print(e)
        print('PushMsg: {}'.format(Msg))


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    #print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'

msg_queue = []
soil_temp, co2, moisture, luminance, aqi, aqi_value = [], [], [], [], [], []

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_id_set
    Msg = event.message.text
#    if Msg == 'Hello, world': return
    print('Incoming Msg: {}'.format(Msg))
    msg_queue.append(Msg)
    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)
    
    if(Msg == 'Temperature'):
        t = soil_temp[-1]
        temp_message = f'目前溫度為 {t} 度，'
        if(t != None):
            if(t < 20):
                temp_message += "\n🥶溫度過低，請啟動加溫設備，並請將對外通風門窗關閉。"
            elif(t > 25):
                temp_message += "\n🥵溫度過高，請啟動冷卻設備，或是開啟通風處喔。"
            else:
                temp_message += "\n😊目前為舒適溫度，無須擔心你的植物們喔。"
        else:
            temp_message = "⚠️目前無法取得溫度資訊，請稍後再查詢～"

        pushLineMsg(temp_message)

    elif(Msg == 'Co2'):
        c = co2[-1]
        co2_message = f'目前二氧化碳濃度為 {c} ppm，'
        if(c != None):
            # if(c < 20):
            #     message += "\n🥶溫度過低，請啟動加溫設備，並請將對外通風門窗關閉。"
            # elif(c > 25):
            #     message += "\n🥵溫度過高，請啟動冷卻設備，或是開啟通風處喔。"
            # else:
            #     message += "\n😊目前為舒適溫度，無須擔心你的植物們喔。"
            pass
        else:
            co2_message = "⚠️目前無法取得二氧化碳濃度資訊，請稍後再查詢～"

        pushLineMsg(co2_message)

    elif(Msg == 'Moisture'):
        m = moisture[-1]
        moi_message = f'目前土壤濕度為 {m}%，'
        if(m != None):
            # if(m < 20):
            #     message += "\n🥶溫度過低，請啟動加溫設備，並請將對外通風門窗關閉。"
            # elif(m > 25):
            #     message += "\n🥵溫度過高，請啟動冷卻設備，或是開啟通風處喔。"
            # else:
            #     message += "\n😊目前為舒適溫度，無須擔心你的植物們喔。"
            pass
        else:
            moi_message = "⚠️目前無法取得土壤濕度資訊，請稍後再查詢～"

        pushLineMsg(moi_message)

    elif(Msg == 'Luminance'):
        l = luminance[-1]
        lum_message = f'目前日照亮度為 {l} lux。。'
        if(l != None):
            # if(l < 20):
            #     message += "\n🥶溫度過低，請啟動加溫設備，並請將對外通風門窗關閉。"
            # elif(l > 25):
            #     message += "\n🥵溫度過高，請啟動冷卻設備，或是開啟通風處喔。"
            # else:
            #     message += "\n😊目前為舒適溫度，無須擔心你的植物們喔。"
            pass
        else:
            lum_message = "⚠️目前無法取得日照亮度資訊，請稍後再查詢～"

        pushLineMsg(lum_message)

    elif(Msg == 'AQI'):
        a = aqi[-1]
        a_value = aqi_value[-1]
        aqi_message = a
        if(a != None and a_value != None):
            if a_value >= 0 and a_value <= 50:
                aqi_message += "\n\n" + "🌱建議措施: \n1️⃣正常進行農事活動，無需特殊處理。\n2️⃣定期檢查作物健康狀況，確保生長條件穩定。\n3️⃣持續監測空氣品質，以預防未來可能的污染。"
            elif a_value > 50 and a_value <= 100:
                aqi_message += "\n\n" + "🌱建議措施: \n1️⃣注意觀察敏感作物（如豆類、番茄等）的葉片變化，防止早期損傷。\n2️⃣適當增加灌溉頻率，清洗植物表面的顆粒物。\n3️⃣考慮在高污染時間段（如中午）減少戶外農事操作。"
            elif a_value > 100 and a_value <= 150:
                aqi_message += "\n\n" + "🌱建議措施: \n1️⃣為敏感作物提供遮陽網或臨時保護性結構，減少直接暴露於污染物中。\n2️⃣增加葉面肥噴灑，補充植物營養，提升抗性。\n3️⃣避免在污染高峰期進行施肥或農藥噴灑，防止與污染物產生化學反應。"
            elif a_value > 150 and a_value <= 200:
                aqi_message += "\n\n" + "🌱建議措施: \n1️⃣加強植物表面清洗，防止污染物積累。\n2️⃣使用抗污染植物品種，減少高敏感作物的栽培。\n3️⃣停止修剪或其他可能引起植物傷口的操作，避免進一步損害。\n4️⃣增加溫室或遮罩結構的使用。"
            elif a_value > 200 and a_value <= 300:
                aqi_message += "\n\n" + "🌱建議措施: \n1️⃣暫停所有戶外農事活動，避免污染物直接損害作物。\n2️⃣使用滴灌或微灌技術清除葉片和莖部的污染物。\n3️⃣在可能的情況下，提前採收成熟作物，減少損失。\n4️⃣避免種植高經濟價值但敏感的作物，改種耐污染品種。"
            else:
                aqi_message += "\n\n" + "🌱建議措施: \n1️⃣將作物完全覆蓋或移入溫室（若條件允許）。\n2️⃣停止一切栽培活動，等待污染緩解。\n3️⃣進行土壤檢測，評估污染物沉積情況，必要時採取土壤修復措施。\n4️⃣評估農田長期影響，考慮輪作或休耕來恢復土壤和植物健康。"
        else:
            aqi_message = "⚠️目前無法取得空氣品質資訊，請稍後再查詢～"

        pushLineMsg(aqi_message)

    else:
        pushLineMsg("無法查詢此項目喔")
    
    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!"))   # reply api example
    # print(f"weather_info: {weather_info}")

def init(port=32768):    
    pushLineMsg('LineBot is ready.')
    app.run('127.0.0.1', port=port, threaded=True, use_reloader=False)

def add_soil_temp(t):
    print('add_soil_temp')
    soil_temp.append(t)

def add_co2(c):
    print('add_co2')
    co2.append(c)

def add_moisture(m):
    print('add_moisture')
    moisture.append(m)

def add_luminance(l):
    print('add_luminance')
    luminance.append(l)

def add_aqi(a, a_value):
    print('add_aqi')
    aqi.append(a)
    aqi_value.append(a_value)

idList = loadUserId()
if idList: user_id_set = set(idList)                   
if __name__ == "__main__":
    init()
    

    
