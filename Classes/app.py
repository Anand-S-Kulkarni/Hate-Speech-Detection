import os
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
from flask import Flask,render_template,request,jsonify
import dash_bootstrap_components as dbc
import model

import sys
import tweepy
import json
import pandas as pd
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config["suppress_callback_exceptions"] = True

track=''

def hatetrack():
    import sqlite3
    import pickle
    import tweepy
    import csv
    from authentication import Authenticate
    from concurrent.futures import ThreadPoolExecutor
    from concurrent import futures

    global model

    conn = sqlite3.connect('C:/sqlite-tools-win32-x86-3310100/shivdeep.db', check_same_thread=False)
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
                argum2 = (status.user.id_str,)
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
            query5 = "update user_track set total_count = total_count+1 where user_id= ?"
            argum5 = (status.user.id_str,)
            try:
                cur.execute(query5, argum5)
                print("Normal Total Count Incremented..!")
                conn.commit()
            except:
                print("Nai Jamla, parat chal")

        def on_error(self, status_code):
            if status_code == 420:
                return False


    stream_listener = CustomStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)


    def follow_tweets(user_id_list):
        #tweet_id = api.get_user(user_id)
        #stream.filter(follow=['1245230935039045632,1223479420146475008'], languages=['en'])
        stream.filter(follow=user_id_list, languages=['en'])

    with open('C:/Users/prati/PycharmProjects/dashboard/venv/dataset/Model.pkl', 'rb') as file:
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
    print("---------------------------------------------------------------------------------------------------------------------",user_id_list)


    #ex = ThreadPoolExecutor(max_workers=5)
    #wait_for = [ex.submit(follow_tweets, i) for i in user_id]
    #for f in futures.as_completed(wait_for):
    #    print(f.running())'''
    follow_tweets(user_id_list)


import sqlite3
conn = sqlite3.connect('C:/sqlite-tools-win32-x86-3310100/shivdeep.db', check_same_thread=False)
print("Opened database successfully" + str(conn))
cur = conn.cursor()

user_list = ['a','s','d','f','g']
user1=""
user2=""
user3=""
user4=""
user5=""
def FetchTopUser():
    cur.execute("select * from user_track order by count desc limit 5")
    user_list = []
    for row in cur.fetchall():
        user_list.append(row[1])
    return user_list

topTrend1=""
consumer_key = 'QmTzLdaUAZ5ueF9U7PRWFqE5w'
consumer_secret = 'x9p285YQCAAmV5Tdi6XioOkFuVeXIQzkhwjAzOHx8220CRjBYF'
access_token = '2928594650-T45h4wTKsV7A77PgzT0icNvLsqTcSePdzLKQ3cj'
access_token_secret = 'zwpq5TbaNS6f7Q9t4A7WVRcXt0IhjDKBvhtpjlQSRS6bh'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

topTrend1=""
topTrend2=""
topTrend3=""
topTrend4=""
topTrend5=""

@app.callback(Output('container-button-timestamp', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
#def update_graph_live():

    BRAZIL_WOE_ID = 2282863

    brazil_trends = api.trends_place(BRAZIL_WOE_ID)

    trends = json.loads(json.dumps(brazil_trends, indent=1))
    count=0

    for trend in trends[0]["trends"]:
        if(count < 5):
            if(count==0):
                topTrend1 = trend["name"]
            if(count==1):
                topTrend2 = trend["name"]
            if(count==2):
                topTrend3 = trend["name"]
            if(count==3):
                topTrend4 = trend["name"]
            if(count==4):
                topTrend5 = trend["name"]
            count=count+1


    return [html.Table(className='table table-hover',children=[
            html.Thead(className='text-warning',children=[
                html.Th('ID'),
                html.Th('Topic'),
            ]),
            html.Tbody(id='live-update-text',children=[
                dcc.Location(id='url1', refresh=False),
                html.Tr(children=[
                    html.Td('1'),
                    dcc.Link(html.Td(topTrend1),id='topic1',href='model1'),
                ]),
                html.Tr(children=[
                    html.Td('2'),
                    dcc.Link(html.Td(topTrend2),id='topic2',href='model2'),
                ]),
                html.Tr(children=[
                    html.Td('3'),
                    dcc.Link(html.Td(topTrend3),id='topic3',href='model3'),
                ]),
                html.Tr(children=[
                    html.Td('4'),
                    dcc.Link(html.Td(topTrend4),id='topic3',href='model4'),
                ]),
                html.Tr(children=[
                    html.Td('5'),
                    dcc.Link(html.Td(topTrend5),id='topic4',href='model5'),
                ]),
            ]),
            html.Br(),

        ])]

def page_2_layout_function():

    track = topTrend1
    import pickle
    import tweepy
    from authentication import Authenticate
    import sqlite3
    global model
    try:
        conn = sqlite3.connect('C:/sqlite-tools-win32-x86-3310100/shivdeep.db')
        print("Opened database successfully" + str(conn))
    except Error as e:
        print(e)
    cur = conn.cursor()

    class CustomStreamListener(tweepy.StreamListener):
        def on_status(self, status):
            # print(status.user.id_str+ " " + status.user.name + " " + status.user.screen_name + " " + status.text)
            # print(status)
            if model.predict_classes(str(status.text)) == 1:
                # with open(r'C:\Users\Admin\Desktop\HateSpeech\dataset\blake.txt' , 'a' , encoding="UTF-8") as f:
                # f.write("%s,%s,%s\n"%(status.user.id,status.user.name,status.text))
                # f.write(status)
                print(str(status.text))
                if(cur.execute("select count(*) from user_track where user_id = ?", (status.user.id_str,))):
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
                    except:
                        print("try harder nigga..!")
                else:
                    query1 = '''insert into user_track(user_id,user_name,screen_name,count,latest_tweet_date)
                    values(?,?,?,1,CURRENT_DATE)'''
                    argum1 = (status.user.id_str, status.user.name, status.user.screen_name)
                # query1 = "insert into user_track values('%s','%s','%s',1,curdate())"
                    query2 = '''insert into tweets_track(user_id,tweet_id,tweet_text,date_of_post)
                    values(?,?,?,CURRENT_DATE)'''
                    argum2 = (status.user.id_str, status.id_str, status.text)

                # try:
                    cur.execute(query1, argum1)
                    cur.execute(query2, argum2)
                    print("Enrolled a hatespeech user suspect")
                    conn.commit()
                # except:
                #    print("try harder nigga..!")

        def on_error(self, status_code):
            if status_code == 420:
                return False

    with open(r'D:/Project/HateSpeech/dataset/Model.pkl', 'rb') as file:
        model = pickle.load(file)

    auther = Authenticate()
    auth = tweepy.OAuthHandler(auther.consumer_key, auther.consumer_secret)
    auth.set_access_token(auther.access_token, auther.access_token_secret)
    api = tweepy.API(auth)

    stream_listener = CustomStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=[track], languages=['en'])

    #FetchTopUser()
    #@app.callback(Output('hateUserList', 'children'),
    #          [Input('interval-component', 'n_intervals')])
    #def FetchTopUser(n):
    #cur.execute("select * from user_track order by count desc limit 5")
    #user_list = []
    #for row in cur.fetchall():
    #    user_list.append(row[1])
        #print(user_list)
    #return user_list
    #FetchTopUser()
    #return [
    html.Table(className='table table-hover',children=[
            html.Thead(className='text-warning',children=[
                html.Th('ID'),
                html.Th('Name'),
            ]),
            html.Tbody(children=[
                #FetchTopUser(),
                html.Tr(children=[
                #html.Td(x) for x in topTrend
                html.Td('1'),
                html.Td(user_list[0])
            ]),
            html.Tr(children=[
                html.Td('2'),
                html.Td(user_list[1])
            ]),
            html.Tr(children=[
                html.Td('3'),
                html.Td(user_list[2])
            ]),
            html.Tr(children=[
                html.Td('4'),
                html.Td(user_list[3])
            ]),
            html.Tr(children=[
                html.Td('5'),
                html.Td(user_list[4])
            ]),
        ]),
        html.Br(),
        #   dcc.Input(id="dtrue", type="number",debounce=True, placeholder="Debounce True",min=1, max=6,size='523'),
    ])

#@app.callback(dash.dependencies.Output('dailySalesChart', 'children'),
#              [Input('interval-component2', 'n_intervals')])
def pie():
    import sqlite3
    import matplotlib.pyplot as plt

    try:
        conn = sqlite3.connect('C:/sqlite-tools-win32-x86-3310100/shivdeep.db')
        print("Opened database successfully" + str(conn))
    except Error as e:
        print(e)
    cur = conn.cursor()

    #cur.execute("select user_name,sum(count),total_count from user_track group by user_name order by user_name asc")
    cur.execute("select sum(count) from user_track")
    Hate_Count = int(cur.fetchone()[0])

    cur.execute("select sum(total_count) from user_track")
    Total_Count = int(cur.fetchone()[0])

    Non_Hate_Count = Total_Count - Hate_Count

    # labels = 'Hate', 'Non-Hate'
    # sizes = [Hate_Count, Non_Hate_Count]
    # explode = (0.2, 0)
    # colors = ['red', 'green'];
    data = [
        {
            'values': [Hate_Count,Non_Hate_Count],
            'type': 'pie',
            'labels': ['Hate','Non-Hate'],
            'pull':[0.1],
            'marker_colors':['rgb(56, 75, 126)', 'rgb(18, 36, 37)'],
        },
    ]

    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {

                    'height':300,
                    'width':500,
                    'margin': {
                        'l': 8,
                        'r': 0,
                       'b': 10,
                        't': 10
                    },
                   'legend': {'x': 0, 'y': 1}
                }
            }
        )
    ])
def bar_graph():
    import sqlite3
    from plotly.tools import mpl_to_plotly
    from matplotlib import pyplot as plt
    import numpy as np

    try:
        conn = sqlite3.connect('C:/sqlite-tools-win32-x86-3310100/shivdeep.db')
        print("Opened database successfully" + str(conn))
    except Error as e:
        print(e)

    cursor = conn.execute("Select user_name,count, (total_count-count) from user_track group by user_name")

    hate = []
    non_hate = []
    uname = []
    show_uname = []
    for row in cursor:
        hate.append(int(row[1]))
        non_hate.append(int(row[2]))
        uname.append(row[0])

    ind = np.arange(len(hate))
    import plotly.graph_objects as go
    #animals=['giraffes', 'orangutans', 'monkeys']
    coun=0

    show_uname.append(uname[0])
    show_uname.append(uname[1])
    show_uname.append(uname[2])

    # fig = go.Figure(data=[
    #     go.Bar(name='SF Zoo', x=show_uname, y=hate),
    #     go.Bar(name='LA Zoo', x=show_uname, y=non_hate)
    # ])
    return html.Div([
        dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': show_uname, 'y': hate, 'type': 'bar', 'name': 'Hate'},
                {'x': show_uname, 'y': non_hate, 'type': 'bar', 'name': 'no-Hate'},
            ],
            'layout': {
                #'title': 'Dash Data Visualization',
                'height':300,
                    'width':500,
                    'margin': {
                        'l': 50,
                        'r': 0,
                       'b': 100,
                        't': 0
                    },
            }
        }
        )
    ])
## @app.callback(dash.dependencies.Output('word-cloud', 'children'),
#               [Input('interval-component2', 'n_intervals')])
def show_wordcloud():
    import sqlite3
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    import numpy as np
    import PIL as pil

    try:
        conn = sqlite3.connect('C:/sqlite-tools-win32-x86-3310100/shivdeep.db')
        print("Opened database successfully" + str(conn))
    except Error as e:
        print(e)
    cur = conn.cursor()
    d = {}

    #For Hate Ratio Based wordcloud
    #cur.execute("Select user_name,count*1.0/total_count from user_track")

    #For Hate COunt Based WordCloud
    cur.execute("Select user_name,count from user_track")

    row = cur.fetchone()
    while row is not None:
        d.update({row[0]:row[1]})
        row = cur.fetchone()


    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=d)

    wordcloud.to_file('N.png')
    image = wordcloud.to_image()

    #image.show()
    #html.Img(src=app.get_asset_url('N.png'),style={'height':'100%', 'width':'100%'})
    # plt.figure()
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()
    # print(d)
#image_filename = 'N.png' # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())
import base64
test_png = 'N.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')
def mainPanel():
    return  html.Div(className='main-panel', children=[
                html.Nav(className='navbar navbar-expand-lg navbar-transparent navbar-absolute fixed-top ',
                      id='navigation-example',children=[
                     html.Div(className='container-fluid',children=[
                         html.Div(className='navbar-wrapper',children=[
                             #html.P('Dashboard')
                         ]),
                        html.Div(className='collapse navbar-collapse justify-content-end',children=[
                            html.Form(className='navbar-form',children=[
                                html.Div(className='input-group no-border',children=[
                                    #dbc.Input(type='text',className = 'form-control',placeholder = 'Search...'),
                                    #dbc.Button("Submit",className='btn btn-default btn-round btn-just-icon'),
                                    html.Div(className='ripple-container')
                                ]),
                            ]),
                        html.Ul(className='navbar-nav',children=[
                            html.Li(className='nav-item',children=[
                                html.A(className='nav-link',href='',children=[
                                    html.P('Stats')
                                ]),
                            ]),
                            html.Li(className='nav-item dropdown',children=[
                                html.A(className='nav-link',id="navbarDropdownMenuLink",href='',children=[
                                    html.P('Some Actions')
                                ]),
                            ]),
                            html.Li(className='nav-item',children=[
                                html.A(className='nav-link',href='',children=[
                                    html.P('Account')
                                ]),
                            ]),
                        ]),
                        ]),
                     ]),
                 ]),
            html.Div(className='content',children=[
                html.Div(className='container-fluid',children=[
                    html.Div(className='row',children=[
                        html.Div(className='col-xl-4 col-lg-12',children=[
                            html.Div(className='card card-chart',children=[
                                html.Div(className='card-header card-header-success',children=[
                                    html.Div(className='ct-chart', id='dailySalesChart',children=[
                                        pie(),
                                    ])
                                ]),
                                html.Div(className='card-body',children=[
                                    html.H4('Total % of Hate & Non-Hate Users'),
                                    html.P('')
                                ]),
                                html.Div(className='card-footer',children=[
                                    html.Div(className='stats',children=[
                                        html.P('Pie Diagram')
                                    ]),
                                ]),
                            ]),
                        ]),
                        html.Div(className='col-xl-4 col-lg-12',children=[
                            html.Div(className='card card-chart',children=[
                                html.Div(className='card-header card-header-warning',children=[
                                    html.Div(className='ct-chart', id='websiteViewsChart',children=[
                                       bar_graph(),

                                    ])
                                ]),
                                html.Div(className='card-body',children=[
                                    html.H4('Hate/Non-Hate User Respective to Topic'),
                                    html.P('')
                                ]),
                                html.Div(className='card-footer',children=[
                                    html.Div(className='stats',children=[
                                        html.P('Bar Graph')
                                    ]),
                                ]),
                            ]),
                        ]),

                        # html.Div(className='col-xl-4 col-lg-12',children=[
                        #     html.Div(className='card card-chart',children=[
                        #         html.Div(className='card-header card-header-danger',children=[
                        #             html.Div(className='ct-chart', id='completedTasksChart')
                        #         ]),
                        #         html.Div(className='card-body',children=[
                        #             html.H4('Completed Tasks'),
                        #             html.P('Last Campaign Performance')
                        #         ]),
                        #         html.Div(className='card-footer',children=[
                        #             html.Div(className='stats',children=[
                        #                 html.P('campaign sent 2 days ago')
                        #             ]),
                        #         ]),
                        #     ]),
                        # ]),
                    ]),
                    html.Div(className='row1',children=[
                        html.Div(className='col-xl-3 col-lg-6 col-md-6 col-sm-6',children=[
                            html.Div(className='card card-stats',children=[
                                html.Div(className='card-header card-header-warning card-header-icon',children=[
                                    html.Div(className='card-icon',id='word-cloud',children=[
                                        show_wordcloud(),
                                        html.Img(src='data:image/png;base64,{}'.format(test_base64),style={'height':'50%', 'width':'200%'}),


                                    ]),
                                    # dcc.Interval(
                                    #     id='interval-component2',
                                    #     interval=5*10000, # in milliseconds
                                    #     n_intervals=0
                                    # ),

                                ]),
                                html.Div(className='card-footer',children=[
                                    html.H4('Word Cloud of Usernames'),
                                    html.Div(className='stats',children=[
                                        #html.A(href='#pablo',className='warning-link',label='Get More Space...')
                                        #html.Img(src=app.get_asset_url('N.png'),style={'height':'100%', 'width':'100%'})
                                        #html.P('Word Cloud')
                                    ]),
                                ]),
                            ]),
                        ]),
                        # html.Div(className='col-xl-3 col-lg-6 col-md-6 col-sm-6',children=[
                        #     html.Div(className='card card-stats',children=[
                        #         html.Div(className='card-header card-header-success card-header-icon',children=[
                        #             html.Div(className='card-icon'),
                        #             html.P('Revenue'),
                        #             html.H3('$34,245')
                        #         ]),
                        #         html.Div(className='card-footer',children=[
                        #             html.Div(className='stats',children=[
                        #                 #html.A(href='#pablo',className='warning-link',label='Last 24 Hours...')
                        #             ]),
                        #         ]),
                        #     ]),
                        # ]),
                        # html.Div(className='col-xl-3 col-lg-6 col-md-6 col-sm-6',children=[
                        #     html.Div(className='card card-stats',children=[
                        #         html.Div(className='card-header card-header-danger card-header-icon',children=[
                        #             html.Div(className='card-icon'),
                        #             html.P('Fixed Issues'),
                        #             html.H3('75')
                        #         ]),
                        #         html.Div(className='card-footer',children=[
                        #             html.Div(className='stats',children=[
                        #                 #html.A(href='#pablo',className='warning-link',label='Tracked from Github...')
                        #             ]),
                        #         ]),
                        #     ]),
                        # ]),
                        # html.Div(className='col-xl-3 col-lg-6 col-md-6 col-sm-6',children=[
                        #     html.Div(className='card card-stats',children=[
                        #         html.Div(className='card-header card-header-info card-header-icon',children=[
                        #             html.Div(className='card-icon'),
                        #             html.P('Followers'),
                        #             html.H3('+245')
                        #         ]),
                        #         html.Div(className='card-footer',children=[
                        #             html.Div(className='stats',children=[
                        #                 #html.A(href='#pablo',className='warning-link',label='Just Updated...')
                        #             ]),
                        #         ]),
                        #     ]),
                        # ]),
                    ]),
                    html.Div(className='row',children=[
                        html.Div(className='col-lg-6 col-md-12',children=[
                            html.Div(className='card',children=[
                                html.Div(className='card-header card-header-primary',children=[
                                    html.H4('Trending Topic'),
                                    html.P('Latest Trending Topic on the Twitter')
                                ]),
                                html.Div(id='container-button-timestamp',className='card-body table-responsive', children=[


                                ]),
                                dcc.Interval(
                                    id='interval-component',
                                    interval=1*10000, # in milliseconds
                                    n_intervals=0
                                ),
                            ])  ,
                        ]),
                        html.Div(id='page-content',className='col-lg-6 col-md-12',children=[
                            html.Div(className='card',children=[
                                html.Div(className='card-header card-header-tabs card-header-warning',children=[
                                     html.H4('Hate User'),
                                    html.P('Latest hate Spreading User on the Twitter'),
                                ]),
                                dcc.Interval(
                                    id='interval-component1',
                                    interval=10*10000, # in milliseconds
                                    n_intervals=0
                                ),
                                html.Div(id='hateUser',className='card-body table-responsive'),
                                    #html.Div(id='hateUserList',className='card-body table-responsive'),


                                #]),
                                ])
                        ]),
                        ]),
                    #html.Div(id='page-content-model'),
                    ])
                ])
            ])


from multiprocessing import Process
import os
import time
def func1():
    for i in range(10000000):
        os.system('python HateTrack2.py')
        time.sleep(1)

def func2():
  #print ('func2: starting')
    for i in range(10000000):
        cur.execute("select * from user_track order by count desc limit 5")
        #global user_list
        user_list = []
        for row in cur.fetchall():
            user_list.append(row[1])
            time.sleep(1)

def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        #p.join()
        cur.execute("select * from user_track order by count desc limit 5")
        #global user_list
        user_list = []
        for row in cur.fetchall():
            user_list.append(row[1])
            time.sleep(1)
        return[
            html.Table(className='table table-hover',children=[
            html.Thead(className='text-warning',children=[
               html.Th('ID'),
                html.Th('Name'),
            ]),
            html.Tbody(children=[
                #FetchTopUser(),
                html.Tr(children=[
                #html.Td(x) for x in topTrend
                html.Td('1'),
                html.Td(user_list[0]),

            ]),
            html.Tr(children=[
                html.Td('2'),
                html.Td(user_list[1])
            ]),
            html.Tr(children=[
                html.Td('3'),
                html.Td(user_list[2])
            ]),
            html.Tr(children=[
                html.Td('4'),
                html.Td(user_list[3])
            ]),
            html.Tr(children=[
                html.Td('5'),
                html.Td(user_list[4])
            ]),
        ]),
        html.Br(),
        #   dcc.Input(id="dtrue", type="number",debounce=True, placeholder="Debounce True",min=1, max=6,size='523'),
        ])]
count=0
def page_2_layout_function():
    #if __name__ == '__main__':

    return[
            html.Table(className='table table-hover',children=[
            html.Thead(className='text-warning',children=[
               html.Th('ID'),
                html.Th('Name'),
            ]),
            html.Tbody(children=[
                #FetchTopUser(),
                html.Tr(children=[
                #html.Td(x) for x in topTrend
                html.Td('1'),
                html.Td(user1),

            ]),
            html.Tr(children=[
                html.Td('2'),
                html.Td(user2)
            ]),
            html.Tr(children=[
                html.Td('3'),
                html.Td(user3)
            ]),
            html.Tr(children=[
                html.Td('4'),
                html.Td(user4)
            ]),
            html.Tr(children=[
                html.Td('5'),
                html.Td(user5)
            ]),
        ]),
        html.Br(),
        #   dcc.Input(id="dtrue", type="number",debounce=True, placeholder="Debounce True",min=1, max=6,size='523'),
        ])]

count=0
page_2_layout = page_2_layout_function()
@app.callback(dash.dependencies.Output('hateUser', 'children'),
              [dash.dependencies.Input('url1', 'pathname'),Input('interval-component1', 'n_intervals')])
def display_page_list(pathname,n):
    if pathname == '/model1':
        track = topTrend1
        global count
        #user_list = runInParallel(func1, func2)
        if(count==0):
            os.system('python Model4.py')
            runInParallel(func1, func2)
            count = count+1
        #return runInParallel(func1, func2)
        else:
            return model.layout
    elif pathname == '/model2':
        track=topTrend2
        #global count
        #user_list = runInParallel(func1, func2)
        if(count==0):
            os.system('python Model4.py')
            runInParallel(func1, func2)
            count = count+1
        #return runInParallel(func1, func2)
        else:
            return model.layout
    elif pathname == '/model3':
        track=topTrend3
        #global count
        #user_list = runInParallel(func1, func2)
        if(count==0):
            os.system('python Model4.py')
            runInParallel(func1, func2)
            count = count+1
        #return runInParallel(func1, func2)
        else:
            return model.layout
    elif pathname == '/model4':
        track=topTrend4
        #global count
        #user_list = runInParallel(func1, func2)
        if(count==0):
            os.system('python Model4.py')
            runInParallel(func1, func2)
            count = count+1
        #return runInParallel(func1, func2)
        else:
            return model.layout
    elif pathname == '/model5':
        track=topTrend5
        #global count
        #user_list = runInParallel(func1, func2)
        if(count==0):
            os.system('python Model4.py')
            runInParallel(func1, func2)
            count = count+1
        #return runInParallel(func1, func2)
        else:
            return model.layout

page_1_layout =mainPanel()
#page_2_layout = page_2_layout_function()

@app.callback(dash.dependencies.Output('page-content2', 'children'),
              [dash.dependencies.Input('url', 'pathname')],)
def display_page(pathname):
    if pathname == '/page-2':
        return page_1_layout
    #elif pathname == '/model':
    #    return page_2_layout

def forRefresh():
    return html.Div( className="wrapper", children=[
    html.Div( style={'background-color':'#808080'},
        className="sidebar",children=[
            html.Div(className='sidebar-wrapper',children=[
                    html.Ul(className="nav",children=[
                        html.Li(className="nav-item active",children=[
                            #html.A(className='nav-link',href='./newfile.py', target="_blank",children=[
                               # dcc.Location(id='url', refresh=False),
                                dcc.Link("Dashboard",href="/page-1",className="nav-link"),
                                html.Div(id='page-content1'),
                        ]),
                        html.Li(className='nav-item', children=[
                                dcc.Location(id='url', refresh=False),
                            html.Div([
                                html.Div([
                                dcc.Link("User Profile",href="/page-2",className="nav-link"),
                                #html.Div(id='page-content2'),
                            #html.P('User Profile')
                                    ]),]),
                             ]),
                            #]),
                        # html.Li(className='nav-item', children=[
                        #         #dcc.Location(id='url3', refresh=False),
                        #         dcc.Link("Table List",href="/page-3",className="nav-link"),
                        #         html.Div(id='page-content3'),
                        #     #html.P('Table List')
                        #      ]),
                        #     #]),
                        # html.Li(className='nav-item', children=[
                        #        #dcc.Location(id='url4', refresh=False),
                        #         dcc.Link("Typography",href="/page-4",className="nav-link"),
                        #         html.Div(id='page-content4'),
                        #     #html.P('Typography')
                        #      ]),
                            ##]),
                         # html.Li(className='nav-item', children=[
                         #        #dcc.Location(id='url5', refresh=False),
                         #        dcc.Link("IIcons",href="/page-5",className="nav-link"),
                         #        html.Div(id='page-content5'),
                         #   # html.P('IIcons')
                         #     ]),
                            #]),
                         # html.Li(className='nav-item', children=[
                         #        #dcc.Location(id='url6', refresh=False),
                         #        dcc.Link("Maps",href="/page-6",className="nav-link"),
                         #        html.Div(id='page-content6'),
                         #    #html.P('Maps')
                         #     ]),
                            #]),
                        ]),
                    ]),
                ]),

        html.Div(id='page-content2'),
            ])
app.layout = forRefresh

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050,threaded=True)
