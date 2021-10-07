import pickle
import tweepy
from authentication import Authenticate
import sqlite3

global model
# conn = pymysql.connect(host='localhost', database='shivdeep', user='root', password='ShivikshaSC2201')
try:
    conn = sqlite3.connect('C:/sqlite-tools-win32-x86-3310100/shivdeep.db')
    print("Opened database successfully" + str(conn))
except Error as e:
    print(e)
cur = conn.cursor()

with open(r'C:\Users\prati\PycharmProjects\dashboard\venv\dataset\Model.pkl', 'rb') as file:
    model = pickle.load(file)

auther = Authenticate()
auth = tweepy.OAuthHandler(auther.consumer_key, auther.consumer_secret)
auth.set_access_token(auther.access_token, auther.access_token_secret)
api = tweepy.API(auth)

j=1
for status in tweepy.Cursor(api.search, lang = "en", q="#corona -filter:retweets", rpp=100,).items(200):
    print(status.user.id_str+ " " + status.user.name + " " + status.user.screen_name + " " + status.text)
    if model.predict_classes(str(status.text)) == 1:
    # with open(r'C:\Users\Admin\Desktop\HateSpeech\dataset\blake.txt' , 'a' , encoding="UTF-8") as f:
    # f.write("%s,%s,%s\n"%(status.user.id,status.user.name,status.text))
    # f.write(status)
        print(str(status.text))
        if(cur.execute("select count(*) from user_track where user_id = ?", (status.user.id_str,)).fetchone()[0]):
            query3 = '''insert into tweets_track(user_id,tweet_id,tweet_text,date_of_post)
                                 values(?,?,?,CURRENT_DATE)'''
            argum3 = (status.user.id_str, status.id_str, status.text)
            print(argum3)
            query4 = "update user_track set count = count + 1 where user_id = ?"
            argum4 = (status.user.id_str,)
            print(argum4)
            try:
                cur.execute(query3, argum3)
                print('done1...')
                cur.execute(query4, argum4)
                print("done2...")
                conn.commit()
                print("enrolled tweet and updated count successfully")
                print(j)
                j = j+1
            except:
                print("try harder nigga..!")
        else:
            query1 = '''insert into user_track(user_id,user_name,screen_name,count,latest_tweet_date,total_count)
            values(?,?,?,1,CURRENT_DATE,0)'''
            argum1 = (status.user.id_str, status.user.name, status.user.screen_name)

            query2 = '''insert into tweets_track(user_id,tweet_id,tweet_text,date_of_post)
            values(?,?,?,CURRENT_DATE)'''
            argum2 = (status.user.id_str, status.id_str, status.text)
            try:
                cur.execute(query1, argum1)
                cur.execute(query2, argum2)
                print("Enrolled a hatespeech user suspect")
                conn.commit()
            except:
                print("try harder nigga..!")

        query5 = "update user_track set total_count = total_count+1 where user_id= ?"
        argum5 = (status.user.id_str,)
        try:
            cur.execute(query5,argum5)
            print("Normal Total Count Incremented..!")
            conn.commit()
        except:
            print("Nai Jamla, parat chal")


