from flask import Flask, request, render_template
import psycopg2
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz
import os

app = Flask(__name__)
DBCONNSTR=os.environ['DBCONNSTR']
#DBCONNSTR is set in the DigitalOcean App setting environment variable as:
#postgres://{username}:{password}@{cockroachcloudhostname}:26257/{clustername}.{databasename}?sslmode=require
#postgres://{username}:{password}@free-tier4.aws-us-west-2.cockroachlabs.cloud:26257/{clustername}.defaultdb?sslmode=require


job_site_patterns = """\"postUrl\" LIKE '%greenhouse%' 
    OR \"postUrl\" LIKE '%lever.co%' 
    OR \"postUrl\" LIKE '%ultipro.com%' 
    OR \"postUrl\" LIKE '%avature.net%'
    OR \"postUrl\" LIKE '%workday.com%' 
    OR \"postUrl\" LIKE '%recruiterbox.com%' 
    OR \"postUrl\" LIKE '%jobvite.com%' 
    OR \"postUrl\" LIKE '%applytojob.com%' 
    OR \"postUrl\" LIKE '%careerarc.com%' 
    OR \"postUrl\" LIKE '%smartrecruiters.com%' 
    OR \"postUrl\" LIKE '%recruitee.com%' 
    OR \"postUrl\" LIKE '%jobscore.com%' 
    OR \"postUrl\" LIKE '%work4labs.com%' 
    OR \"postUrl\" LIKE '%jobs.ac.uk%' 
    OR \"postUrl\" LIKE '%workable.com%' 
    OR \"postUrl\" LIKE '%brassring.com%' 
    OR \"postUrl\" LIKE '%softgarden.com%'
    OR \"postUrl\" LIKE '%careers.%.edu%' 
    OR \"postUrl\" LIKE '%jobs.%.edu%' 
    OR \"postUrl\" LIKE '%careers.%.ac.%' 
    OR \"postUrl\" LIKE '%jobs.%.ac.%' 
    OR \"postUrl\" LIKE '%jobarxiv.org%'"""

job_site_patterns = """
    OR \"postUrl\" LIKE '%careers.%.edu%' 
    OR \"postUrl\" LIKE '%jobs.%.edu%' 
    OR \"postUrl\" LIKE '%careers.%.ac.%' 
    OR \"postUrl\" LIKE '%jobs.%.ac.%' 
    """


@app.route('/')
def index():
    sql_stmt = "SELECT title, \"postUrl\", timestamp, replace(twitter_user, 'H/T: ', ''), rowid FROM openstatistics.rssitems WHERE (" + job_site_patterns + ") AND starred=1  ORDER BY TIME DESC"


    try:
        conn = psycopg2.connect(DBCONNSTR)
        print("connected" )
    except:
        print ("I am unable to connect to the database" )
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
    except:
        print ("I am unable to connect to the database")
    mycursor =conn.cursor()
    mycursor.execute(sql_stmt)
    data = mycursor.fetchall()
    mycursor.close()
    conn.close()



    return render_template('index.html', data=data, title="HiveMined - " +data[0][0], heading =data[0][0])



@app.route('/feed')
def feed():

    sql_stmt = "SELECT title, \"postUrl\", timestamp, replace(twitter_user, 'H/T: ', ''), rowid FROM openstatistics.rssitems WHERE ("  + job_site_patterns + " ) AND starred=1  ORDER BY TIME DESC LIMIT 30" 
    try:
        conn = psycopg2.connect(DBCONNSTR)
        print("connected")
    except:
        print ("I am unable to connect to the database")
    mycursor =conn.cursor()
    mycursor.execute(sql_stmt)
    posts = mycursor.fetchall()
    mycursor.close()
    conn.close()


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

