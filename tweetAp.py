
import tweepy
import random
import time
from datetime import datetime

api_key = ''
api_key_secret = ''
access_token = ''
access_token_secret= ''

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Dice val
rand = random.randrange(1,10)
str1 = '다이스 결과는',str(rand)
str1 = ' '.join(str1)

# Time var
now=datetime.now()
current_time=now.strftime("%H:%M:%S")

fileName = 'lastID.txt'
# Funtion to save the last id
def saveLastId(lastId, fileName):
    f_write = open(fileName, 'w')
    f_write.write(str(lastId))
    f_write.close()
    return

# Function to read last id
def readLastId(fileName):
    f_read = open(fileName, 'r')
    ultimo_id_lido = int(f_read.read().strip())
    f_read.close()
    return ultimo_id_lido

def reply():
    try:
        print('BOT WORKING')
        lastId = readLastId(fileName)
        mentions = api.mentions_timeline(lastId, tweet_mode = 'extended')
        for mention in reversed(mentions):
            if '@yourbot'.upper() in mention.full_text.upper():
                lastId = mention.id
                print(str(mention.id) + '-' + mention.full_text)
                saveLastId(lastId, fileName)
                print('Answering tweet')
                message = '@{} {fname} 님에게 답글 테스트 시작 '.format(mention.user.screen_name, fname=mention.user.name)
                api.update_status(status = message, in_reply_to_status_id = mention.id)
    except tweepy.TweepError as e:
          print (e.reason)
            


while True:
    reply()
    time.sleep(30)
