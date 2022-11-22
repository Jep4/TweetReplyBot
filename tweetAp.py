import tweepy
import time
import datetime
from pytz import timezone

import random
import requests
import json
import gspread
import sys

sys.path.append("/home/ubuntu/.local/lib/python3.5/site-packages")


API_KEY = ""
API_KEY_SECRET = ""
USER_ACCESS_TOKEN = ""
USER_ACCESS_SECRET = ""

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET, 'oob')
auth.set_access_token(USER_ACCESS_TOKEN, USER_ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

gc = gspread.service_account(filename='avian-influence-353716-f0c191e15f10.json')

wks = gc.open("")

city = "Seoul" 
apikey = ""
lang = "kr"  

weather_api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"  # 그대로 놔두세요!

result = requests.get(weather_api)
data = json.loads(result.text)


text_list4 = "아오조라의 날씨입니다. \n날씨는 " + data["weather"][0]["description"] + "입니다.\n현재 온도는 " + str(
    data["main"]["temp"]) + "°C 입니다. \n체감 온도는 " + str(data["main"]["feels_like"]) + "°C."


bot = api.verify_credentials()  
bot_id = bot.id  
timeline_list = api.user_timeline(user_id=bot_id)

last_reply_id = timeline_list[0].id_str 



def select_sheet(sheet_name):
    worksheet = wks.worksheet(sheet_name)
    return worksheet



def check_new_mention():
    global last_reply_id
    mention_return = api.mentions_timeline(since_id=last_reply_id)  
    mention_return_length = len(mention_return)  

    if mention_return_length > 0:
        check_keyword(mention_return_length, mention_return) 
        return  




def check_keyword(mention_return_length, mention_return):
    global last_reply_id

    for i in range(mention_return_length - 1, -1, -1):  
        mention = mention_return[i]  
        mention_text = mention.text 
        keyword_type = -1 
        reply_content = ""  
        keyword_action_return = ''

        print("마지막 답멘 =" + mention_text)
        if mention.author.id != bot_id:  
            if '날씨' in mention_text or '날씨' == mention_text:
                reply_content = text_list4
                reply_function(mention, reply_content)

            elif 'Shop' in mention_text or 'Shop' == mention_text:
                worksheet = select_sheet('Shop')
                all_info = worksheet.get_all_values()

                reply_content = ''
                ran = random.randrange(0, 32)
                stuff = all_info[ran][0]
                price = all_info[ran][1]
                price = all_info[ran][1]
                reply_content += stuff + "(이/가) 나왔다! 가격은 " + price + "코인이다. \n구매할까?"

                reply_function(mention, reply_content)

            elif '자판기' in mention_text or '자판기' == mention_text:
                worksheet = select_sheet('이벤트')
                all_info = worksheet.get_all_values()

                reply_content = ''
                ran = random.randrange(0, 15)
                stuff = all_info[ran][0]
                price = all_info[ran][1]
                exp = all_info[ran][2]
                reply_content += stuff + "(이/가) 나왔다! 가격은 " + price + "코인이다. \n" + exp

                reply_function(mention, reply_content)

            elif '운세' in mention_text or '운세' == mention_text:
                worksheet = select_sheet('운세')
                all_info = worksheet.col_values(1)
                reply_content = ''
                reply_content += mention.author.name + "님의 운세는: "
                reply_content += str(random.choice(all_info))

                reply_function(mention, reply_content)

            else:
                reply_content = ''
                reply_function(mention, reply_content)
                return


def roll_dice(mention_keyword):
    dice_info = []
    dice_result_list = []

    if len(mention_keyword) > 1:  
        second_keyword = mention_keyword[
            1].strip() 

        if 'd' in second_keyword: 
            dice_info = second_keyword.split('d') 
        elif 'D' in second_keyword: 
            dice_info = second_keyword.split('D') 

        if len(dice_info) == 2:
            try:
                dice_f_num = int(dice_info[0])  
                dice_s_num = int(dice_info[1]) 
                for _ in range(dice_f_num): 
                    dice = random.randrange(1, dice_s_num + 1)  
                    dice_result_list.append(dice)  
                return dice_f_num, dice_s_num, dice_result_list 
            except:
                print("에러 발생")
                pass

    print("! 다이스 키워드가 잘못됐습니다")
    return (-1, -1, -1)


def reply_function(mention, reply_content):
    global last_reply_id

    reply_to = "@" + mention.author.screen_name + ' ' 
    now = datetime.datetime.now(timezone('Asia/Seoul'))
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    total_reply_content = reply_to + reply_content + '\n\n' + nowDatetime  
    api.update_status(total_reply_content, in_reply_to_status_id=mention.id_str) 

    last_reply_id = mention.id_str  

    return


def err_function(mention, reply_content):
    global last_reply_id

    reply_to = "@" + mention.author.screen_name + ' ' 
    now = datetime.datetime.now(timezone('Asia/Seoul'))
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    total_reply_content = reply_to + reply_content + '\n\n' + nowDatetime  

    last_reply_id = mention.id_str  

    return


def start_time():
    now = datetime.datetime.now(timezone('Asia/Seoul')) 
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')  
    api.update_status("통금 시간입니다.(01:00~06:00)\n" + nowDatetime)


def end_time():
    now = datetime.datetime.now(timezone('Asia/Seoul'))
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    api.update_status("모든 트윗을 허용합니다.\n" + nowDatetime)


while True:
    now2 = datetime.datetime.now(timezone('Asia/Seoul'))
    if now2.strftime('%H:%M') == '06:00':
        end_time()

    if now2.strftime('%H:%M') == '01:00':
        start_time()

    check_new_mention()
    time.sleep(45)
