#IMPORT SECTION
import time
import datetime
import sys
import os
import json
import pprint
import urllib.request
import sqlite3
from datetime import datetime

#Loop run every 5 minutes


last_minute = 1000

while True :
    time.sleep(10)
    now_minute = datetime.now().minute
    # print("last_minute :" + str(last_minute) + " "  + "now_minute : " + str(now_minute))
    if last_minute != 1000:
        if ( now_minute == last_minute  + 1 ):
            print("insert")

            conn = conn = sqlite3.connect('db.sqlite3')
            x = conn.cursor()

            try:
                url = 'https://poloniex.com/public?command=returnTicker'
                # response = http.request('GET', url)
                # data = response.data.decode("utf-8")
                # print((data))
                sock = urllib.request.urlopen(url)
                htmlSource = sock.read()
                sock.close()
                # print(htmlSource)
                json_resp = json.loads(htmlSource)
                for key in json_resp:
                    baseVolume = json_resp[key]["baseVolume"]
                    last = json_resp[key]["last"]
                    quoteVolume = json_resp[key]["quoteVolume"]
                    x.execute("""INSERT INTO prices VALUES (%s,%s,%s,%s,%s)""",
                              (str(datetime.now()), key, baseVolume, last, quoteVolume))
                    conn.commit()
            except:
                conn.rollback()

            conn.close()
            last_minute = now_minute
    else:
        print(str(datetime.now()))

        conn = sqlite3.connect('db.sqlite3')
        x = conn.cursor()

        try:
            url = 'https://poloniex.com/public?command=returnTicker'
            # response = http.request('GET', url)
            # data = response.data.decode("utf-8")
            # print((data))
            sock = urllib.request.urlopen(url)
            htmlSource = sock.read()
            sock.close()
            # print(htmlSource)
            json_resp = json.loads(htmlSource)
            for key in json_resp:
                baseVolume = json_resp[key]["baseVolume"]
                last = json_resp[key]["last"]
                quoteVolume = json_resp[key]["quoteVolume"]
                x.execute("""INSERT INTO prices VALUES (%s,%s,%s,%s,%s)""",
                          (str(datetime.now()), key, baseVolume, last, quoteVolume))
                conn.commit()
        except:
            conn.rollback()

        conn.close()
        last_minute = now_minute
        print("first")
