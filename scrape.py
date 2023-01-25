#!/usr/bin/env python3.8
import snscrape.modules.twitter as sntwitter
import pymysql.cursors
from config import *

query = "(amazon delivery or Amazon delivery or Amazon Prime) until:2020-01-01 since:2010-01-01 lang:en"
date = []
username = []
tweets = []


limit = 20000


for tweet in sntwitter.TwitterSearchScraper(query).get_items():

    if len(tweets) == limit:
        break
    date.append(tweet.date)
    username.append(tweet.user.username)
    tweets.append(tweet.rawContent)



columns = ['date','username','tweet']
connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database=database,
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        sql = f"INSERT INTO tweets ({columns[0]}, {columns[1]}, {columns[2]}) VALUES (%s, %s, %s)"
        # Iterate through the lists and insert each value into the database
        for i in range(len(tweets)):
            cursor.execute(sql, (date[i],username[i],tweets[i]))
            print(f'line : {i}')
        print(len(tweets[1]))
        # Commit the changes
        connection.commit()
        
        print("Done!")
        print(f'Number of tweets scraped: {len(tweets)}')
        # Close the cursor and the connection
        cursor.close()
