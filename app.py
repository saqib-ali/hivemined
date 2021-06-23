from flask import Flask, request, render_template
import psycopg2
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz
import os
import time
import logging


app = Flask(__name__)
DBCONNSTR=os.environ['DBCONNSTR']
#DBCONNSTR is set in the DigitalOcean App setting environment variable as:
#postgres://{username}:{password}@{cockroachcloudhostname}:26257/{clustername}.{databasename}?sslmode=require
#postgres://{username}:{password}@free-tier4.aws-us-west-2.cockroachlabs.cloud:26257/{clustername}.defaultdb?sslmode=require



job_site_patterns = """
    
    \"postUrl\" LIKE '%careers.%.edu%' 
    OR \"postUrl\" LIKE '%jobs.%.edu%' 
    OR \"postUrl\" LIKE '%opportunities.%.edu%' 
    OR \"postUrl\" LIKE '%employment.%.edu%' 

    
    OR \"postUrl\" LIKE '%careers.%.ac.%' 
    OR \"postUrl\" LIKE '%jobs.%.ac.%' 
    OR \"postUrl\" LIKE '%opportunities.%.ac.%' 
    OR \"postUrl\" LIKE '%employement.%.ac.%' 

    
    OR \"postUrl\" LIKE '%.ac.%/job%' 
    OR \"postUrl\" LIKE '%.ac.%/career%'
    OR \"postUrl\" LIKE '%.ac.%/Vacanc%' 

    OR \"postUrl\" LIKE '%.edu.%/job%' 
    OR \"postUrl\" LIKE '%.edu.%/career%' 
    OR \"postUrl\" LIKE '%.edu.%/Vacanc%' 
    
    OR \"postUrl\" LIKE '%.edu/job%' 
    OR \"postUrl\" LIKE '%.edu/career%' 
    OR \"postUrl\" LIKE '%.edu/Vacanc%' 

    """


@app.route('/')
def index():
    sql_stmt = "SELECT title, \"postUrl\", timestamp, replace(twitter_user, 'H/T: ', ''), rowid FROM openstatistics.rssitems WHERE (" + job_site_patterns + ") AND starred=1  ORDER BY TIME DESC LIMIT 10"



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
    mycursor.close()
    conn.close()



    return render_template('index.html', data=data, title="HiveMined - " +data[0][0], heading =data[0][0])



@app.route('/feed')
def feed():
    db_start_time = time.time()
    sql_stmt = "SELECT title, \"postUrl\", timestamp, replace(twitter_user, 'H/T: ', ''), rowid FROM openstatistics.rssitems WHERE ("  + job_site_patterns + " ) AND starred=1  ORDER BY TIME DESC LIMIT 10" 
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
    #logging.info('DB SELECT time:' +  str(db_end_time-db_start_time))

    fg = FeedGenerator()
    fg.title('HiveMined - The No-nonsense Job Board')
    fg.link( href='http://hivemined.net', rel='alternate' )
    fg.link( href='http://hivemined.net/feed', rel='self' )
    fg.description('HiveMined - The No-nonsense Job Board')

    for post in posts:
        format = "%Y-%m-%d %H:%M:%S"

#        tz = pytz.timezone('Asia/Kolkata')
#        dateposted = post[2].astimezone(tz) 

        fe = fg.add_entry()
        fe.id(str(post[4]))
        fe.title(post[0])
        fe.description(post[0])
        fe.link(href='http://hivemined.net/' + str(post[4]))

#        fe.pubdate(dateposted)
#        fe.pubDate(dateposted)
#        fe.updated(post[2])




#    for post in posts:

    return fg.rss_str(pretty=True)

