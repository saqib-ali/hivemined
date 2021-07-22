from flask import Flask, request, render_template
import psycopg2
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz
import os
import time
import logging
from flask import send_from_directory


app = Flask(__name__)
DBCONNSTR=os.environ['DBCONNSTR']
#DBCONNSTR is set in the DigitalOcean App setting environment variable as:
#postgres://{username}:{password}@{cockroachcloudhostname}:26257/{clustername}.{databasename}?sslmode=require
#postgres://{username}:{password}@free-tier4.aws-us-west-2.cockroachlabs.cloud:26257/{clustername}.defaultdb?sslmode=require




@app.route('/')
def index():
    sql_stmt = "SELECT title, \"postUrl\", timestamp, replace(twitter_user, 'H/T: ', ''), rowid FROM openstatistics.rssitems WHERE show_on_hivemined=1 AND starred=1  ORDER BY TIME DESC LIMIT 10"



    try:
        conn = psycopg2.connect(DBCONNSTR)
        print("connected" )
    except Exception as e:
        print (e)
    mycursor =conn.cursor()
    mycursor.execute(sql_stmt)
    data = mycursor.fetchall()
    mycursor.close()
    conn.close()


    return render_template('index.html', data=data, title="HiveMined - The No-Nonsense Job Board", heading="HiveMined - The No-Nonsense Job Board")


@app.route('/<post_id>')
def post(post_id):
    sql_stmt = "SELECT title, \"postUrl\", timestamp, replace(twitter_user, 'H/T: ', '')  FROM openstatistics.rssitems WHERE rowid=" + post_id

    try:
        conn = psycopg2.connect(DBCONNSTR)
        print("connected")
    except Exception as e:
        print (e)
    mycursor =conn.cursor()
    mycursor.execute(sql_stmt)
    data = mycursor.fetchall()


    #sql_stmt2 = "SELECT title, \"postUrl\", timestamp, replace(twitter_user, 'H/T: ', ''),  levenshtein(substring('"+data[0][0]+"',0,255), substring(title,0,255)) as dist FROM openstatistics.rssitems WHERE (show_on_hivemined=1) ORDER BY dist ASC, time DESC LIMIT 10"
    #mycursor.execute(sql_stmt2)
    #data2= mycursor.fetchall()
    mycursor.close()
    conn.close()
    return render_template('index.html', data=data,  title="HiveMined - " +data[0][0], heading="HiveMined - The No-Nonsense Job Board")


@app.route('/users/<user_id>')
def usershares(user_id):
    sql_stmt = "SELECT title, \"postUrl\", timestamp, replace(twitter_user, 'H/T: @', '') as twitter_user_id  FROM openstatistics.rssitems WHERE show_on_hivemined=1 AND starred=1 AND twitter_user LIKE '%" + user_id + "'"

    try:
        conn = psycopg2.connect(DBCONNSTR)
        print("connected")
    except Exception as e:
        print (e)
    mycursor =conn.cursor()
    mycursor.execute(sql_stmt)
    data = mycursor.fetchall()

    mycursor.close()
    conn.close()
    return render_template('index.html', data=data,  title="HiveMined - Jobs Shared by " +data[0][3], heading="HiveMined - The No-Nonsense Job Board")



@app.route('/users/)
def usershares(user_id):
    sql_stmt = "SELECT title, \"postUrl\", timestamp, replace(twitter_user, 'H/T: @', '') as twitter_user_id  FROM openstatistics.rssitems WHERE show_on_hivemined=1 AND starred=1"

    try:
        conn = psycopg2.connect(DBCONNSTR)
        print("connected")
    except Exception as e:
        print (e)
    mycursor =conn.cursor()
    mycursor.execute(sql_stmt)
    data = mycursor.fetchall()

    mycursor.close()
    conn.close()
    return render_template('users.html', data=data,  title="HiveMined - Users", heading="HiveMined - The No-Nonsense Job Board")





@app.route('/feed')
def feed():
    db_start_time = time.time()
    sql_stmt = "SELECT title, \"postUrl\", timestamp, replace(twitter_user, 'H/T: ', ''), rowid FROM openstatistics.rssitems WHERE show_on_hivemined=1 AND starred=1  ORDER BY TIME DESC LIMIT 30" 
    try:
        conn = psycopg2.connect(DBCONNSTR)
        print("connected")
    except Exception as e:
        print (e)
    mycursor =conn.cursor()
    mycursor.execute(sql_stmt)
    posts = mycursor.fetchall()
    mycursor.close()
    conn.close()
    db_end_time = time.time()
    print('DB SELECT time:' +  str(db_end_time-db_start_time))

    fg = FeedGenerator()
    fg.title('HiveMined - The No-nonsense Job Board')
    fg.link( href='http://hivemined.net', rel='alternate' )
    fg.link( href='http://hivemined.net/feed', rel='self' )
    fg.description('HiveMined - The No-nonsense Job Board')

    for post in posts:
        format = "%Y-%m-%d %H:%M:%S"

        tz = pytz.timezone('Europe/Amsterdam')
#        tz = pytz.timezone('Asia/Kolkata')
#        dateposted = post[2].astimezone(tz) 

        fe = fg.add_entry()
        fe.id(str(post[4]))
        fe.title(post[0])
        fe.description(post[0])
        fe.link(href='http://hivemined.net/' + str(post[4]))
        fe.pubDate(tz.localize(post[2]))

#        fe.pubdate(dateposted)
#        fe.pubDate(dateposted)
#        fe.updated(post[2])




#    for post in posts:

    return fg.rss_str(pretty=True)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/png')


@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static', 'text'),
                               'robots.txt', mimetype='text/plain')                               