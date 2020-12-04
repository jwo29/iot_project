from flask import Flask, request
from flask import render_template, json
import pymysql

import RPi.GPIO as GPIO

app = Flask(__name__)

db = pymysql.connect(
    host='localhost', 
    user='root', 
    password='1234',
    db='mydb', 
    charset='utf8'
)

cur = db.cursor()

GPIO.setmode(GPIO.BCM)

led = {
    'pin': 23,
    'state': GPIO.LOW
}

resultTime = {
    'from': '0000',
    'to': '0000',
}

GPIO.setup(led['pin'], GPIO.OUT, initial=GPIO.LOW)

@app.route('/')
def home():
    templateData = {'sensor': led}

    return render_template('home.html', **templateData)

@app.route('/sensor/on')
def sensorOn():

    led['state'] = GPIO.HIGH
    GPIO.output(led['pin'], led['state'])

    templateData = {'sensor': led}

    return render_template('home.html', **templateData)

@app.route('/result')
def showResult():
    ''' turn off led and PIR sensor, and then load info from db '''

    # turn off led and PIR sensor
    led['state'] = GPIO.LOW
    GPIO.output(led['pin'], led['state'])
    templateData = {'sensor': led}

    # extract start time, end time from database
    cur.execute("SELECT MIN(time), MAX(time) FROM detect")
    rows = cur.fetchall() # rows = ((start time, end time),)

    sTime, eTime = rows[0][0], rows[0][1]
    resultTime['from'] = sTime[:2] + ':' + sTime[2:] # '00:00'
    resultTime['to'] = eTime[:2] + ':' + eTime[2:] # '00:00'

    # extract times that the body was detected, and these number from database
    cur.execute("SELECT time, COUNT(*) FROM detect GROUP BY time")
    rows = cur.fetchall() # rows = ((time1, count1), (time2, count2), ...)

    # convert rows(tuple) to temp(list) 
    temp = []
    for row in rows:
        temp.append(list(row))
    # temp = [[time1, count1], [time2, count2], ...]

    resultData = json.dumps(temp)
    print(resultData)

    templateData = {'resultTime': resultTime}

    return render_template(
        'result.html', 
        **templateData
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
