import json
import requests
from bs4 import BeautifulSoup

#TOKENを取得
def get_token():
    with open('your jsonfile') as f:
        jsn=json.load(f)
        TOKEN=jsn['TOKEN']
    return TOKEN
        
#翌日の天気の情報を取得
def get_we_info():
    url='https://weather.yahoo.co.jp/weather/jp/26/6110.html'
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')

    #天気の情報を取得
    info_main=soup.find('div',class_='forecastCity')
    date=info_main.find_all('p',class_='date')[1].text.strip()
    weather=info_main.find_all('p',class_='pict')[1].text.strip()
    temp_high=info_main.find_all('li',class_='high')[1].find('em').text+'℃'
    temp_low=info_main.find_all('li',class_='low')[1].find('em').text+'℃'
    
    d={       
        '日付':date,
        '天気':weather,
        '最高気温':temp_high,
        '最低気温':temp_low,
    }

    #雨なら降水確率を取得
    if ('雨' in weather)==True:
        rain_main=info_main.find_all('tr',class_='precip')[1].find_all('td')
        zero_six=rain_main[0].text
        d['0-6']=zero_six
        six_twelve=rain_main[1].text
        d['6-12']=six_twelve
        twelve_eighteen=rain_main[2].text
        d['12-18']=twelve_eighteen
        eighteen_twenty=rain_main[3].text
        d['18-24']=eighteen_twenty
    return d

#lineに送信
def send_message(token,dic):
    
    headers={'Authorization':'Bearer '+token}
    
    text='\n'+dic['日付']+'は'+dic['天気']+'です。\n'+'最高気温:'+dic['最高気温']+'\n'+'最低気温'+dic['最低気温']+'\n'
    
    if ('雨' in dic['天気'])==True:
        text+='降水確率:\n'+'  0~6:'+dic['0-6']+'\n'+'  6~12:'+dic['6-12']+'\n'+'  12~18:'+dic['12-18']+'\n'+'  18~24:'+dic['18-24']

    files={'message':(None,text)}

    requests.post('https://notify-api.line.me/api/notify',headers=headers,files=files)
    
def main():
    
    token=get_token()
    
    dic=get_we_info()
    
    send_message(token,dic)
    
    
if __name__=='__main__':
    main()

