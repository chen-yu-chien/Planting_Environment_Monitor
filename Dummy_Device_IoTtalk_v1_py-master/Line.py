# coding=UTF-8
import requests


def notify(msg):
    token_key = 'tftPUfnQRFJP31n5T9fCttlJbEB1dMeYmVPtZxErK50'
    header = {'Content-Type':'application/x-www-form-urlencoded',"Authorization":'Bearer '+token_key}
    URL = 'https://notify-api.line.me/api/notify'
    payload = {'message':msg}
    res=requests.post(URL,headers=header,data=payload)

if __name__ == '__main__':
    msg = '測試訊息'
    notify(msg)