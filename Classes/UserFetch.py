import sqlite3
conn = sqlite3.connect('C:/sqlite-tools-win32-x86-3310100/shivdeep.db', check_same_thread=False)
print("Opened database successfully" + str(conn))
cur = conn.cursor()
def FetchTopUser():
    cur.execute("select * from user_track order by count desc limit 5")
    user_list = []
    for row in cur.fetchall():
        user_list.append(row[1])
        print(user_list)
    #return user_list
#print(FetchTopUser())
    return [
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
    ])
    ]
FetchTopUser()
