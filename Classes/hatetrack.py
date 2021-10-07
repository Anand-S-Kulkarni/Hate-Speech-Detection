# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 00:37:36 2020

@author: Madhuri
"""

import sqlite3
import pickle
import tweepy
import csv
from authentication import Authenticate
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures

global model

conn = sqlite3.connect('C:/sqlite/sqlite-tools-win32-x86-3310100/shivdeep.db', check_same_thread=False)
print("Opened database successfully" + str(conn))

cur = conn.cursor()
curr = conn.cursor()

auther = Authenticate()
auth = tweepy.OAuthHandler(auther.consumer_key, auther.consumer_secret)
auth.set_access_token(auther.access_token, auther.access_token_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.user.id_str+ " " + status.user.name + " " + status.user.screen_name + " " + status.text)
        if model.predict_classes(str(status.text)) == 1:
            print(status.user.id_str + " " + status.user.name + " " + status.user.screen_name + " " + status.text)
            # with open(r'C:\Users\Admin\Desktop\HateSpeech\dataset\haters.csv', 'a', encoding="UTF-8") as f:
            #    f.write("%s,%d\n"%(status.user.id, status.text))
            query1 = '''insert into tweets_track(user_id,tweet_id,tweet_text,date_of_post)
                         values(?,?,?,CURRENT_DATE)'''
            argum1 = (status.user.id_str, status.id_str, status.text)
            print(argum1)
            query2 = "update user_track set count = count + 1 where user_id = ?"
            argum2 = (status.user.id_str)
            print(argum2)

            try:
                cur.execute(query1, argum1)
                print('done1...')
                cur.execute(query2, argum2)
                print("done2...")
                conn.commit()
                print("enrolled tweet and updated count successfully")
            except:
                print("try harder nigga..!")

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = CustomStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)


def follow_tweets(user_id_list):
    #tweet_id = api.get_user(user_id)
    stream.filter(follow=['1245230935039045632,1223479420146475008'], languages=['en'])
    stream.filter(follow=user_id_list, languages=['en'])

with open('C:/Users/Admin/Desktop/HateSpeech/dataset/Model.pkl', 'rb') as file:
    model = pickle.load(file)

# user_id = []
# with open('C:/Users/Madhuri/Desktop/HateSpeech/dataset/db.csv' , 'r' , encoding="UTF-8") as f:
# csv_reader = csv.reader(f, delimiter=',')
# for i in csv_reader:
# if len(i) > 1:
# user_id.append(i[0])


#Script For Creating a string of  user IDs
user_id_string = ''
cur.execute("select * from user_track")
for row in cur.fetchall():
    if(len(user_id_string)):
        user_id_string = user_id_string + "," + row[0]
    else:
        user_id_string = row[0]

user_id_list = [user_id_string]


#ex = ThreadPoolExecutor(max_workers=5)
#wait_for = [ex.submit(follow_tweets, i) for i in user_id]
#for f in futures.as_completed(wait_for):
#    print(f.running())'''
follow_tweets(user_id_list)