

import tweepy
import sys


def update_tweet(tweet):
    api_key = ''
    api_key_secret = ''
    access_token = '-'
    access_token_secret= ''

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    api.update_status(tweet)
    
update_tweet("¾È³ç")