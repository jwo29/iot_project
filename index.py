#-*- coding: utf-8 -*-
from flask import Flask, request
from flask import render_template, json
import pymysql
import datetime
import time

import RPi.GPIO as GPIO

app = Flask(__name__)

db = pymysql.connect(
    host='localhost',
    user='root', 
    password='1234',
    db='mydb', # mydb 데이터베이스의 detect 테이블을 이용함
    charset='utf8'
)

cur = db.cursor(pymysql.cursors.DictCursor)

resultTime = {
    'from': '00:00',
    'to': '00:00',
}

GPIO.setmode(GPIO.BCM)

# GPIO 핀 설정
red_led = 23
yellow_led = 24
sensor = {
    'pin': 4,
    'state': False
}

# 핀의 IN/OUT 설정
GPIO.setup(red_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(yellow_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(sensor['pin'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def sensor_callback(channel):
    ''' PIR 센서 이벤트 콜백 함수 '''

    # 현재 시간 추출
    now = datetime.datetime.now()
    currentTime = now.strftime('%H:%M') # '00:00'

    # 현재 시간을 DB에 삽입
    cur.execute("INSERT INTO detect VALUES (%s)", (currentTime))
    db.commit() # DB에 반영

    # 노란색 LED가 0.5초 동안 반짝 거림
    GPIO.output(yellow_led, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(yellow_led, GPIO.LOW)


@app.route('/')
def home():
    # sensor 의 상태에 따라 home.html 의 구성이 바뀔 수 있도록 templateData 반환
    templateData = {'sensor': sensor}

    return render_template('home.html', **templateData)


@app.route('/sensor/on')
def sensorOn():
    ''' 센서 작동 시작 '''

    # 빨간색 LED와 센서 켜기(센서: 이벤트 등록)
    GPIO.output(red_led, GPIO.HIGH)
    GPIO.add_event_detect(sensor['pin'], GPIO.RISING, callback=sensor_callback)
    sensor['state'] = True

    # sensor 의 상태에 따라 home.html 의 구성이 바뀔 수 있도록 templateData 반환
    templateData = {'sensor': sensor}

    return render_template('home.html', **templateData)


@app.route('/result')
def showResult():
    ''' 센서 작동을 중지하고, 데이터베이스로부터 레코드 읽어오기 '''

    # LED와 센서 끄기(센서: 이벤트 삭제)
    GPIO.output(red_led, GPIO.LOW)
    GPIO.output(yellow_led, GPIO.LOW)
    GPIO.remove_event_detect(sensor['pin'])
    sensor['state'] = False

    # 데이터베이스로부터 센서가 작동하는 동안 인체가 감지된 처음 시간과 마지막 시간 정보를 가져옴
    cur.execute("SELECT MIN(time) AS 'from', MAX(time) AS 'to' FROM detect")
    rows = cur.fetchall() # rows = [{'from': start_time, 'to': end_time}]

    resultTime['from'] = rows[0]['from'] # '00:00'
    resultTime['to'] = rows[0]['to'] # '00:00'
    
    # 데이터베이스로부터 인체가 감지된 시간과 시간별 감지 횟수 정보를 가져옴
    cur.execute("SELECT time, COUNT(*) AS 'count' FROM detect GROUP BY time")
    rows = cur.fetchall() # rows = [{'time1': count1}, {'time2': count2}, ... ]

    templateData = {'resultTime': resultTime}
    resultData = rows
    
    return render_template(
        'result.html', 
        **templateData,
        resultData = resultData
    )


@app.route('/removeall')
def removeAll():
    ''' 모든 레코드 삭제, LED, 센서 작동 중지 및 메인 화면으로 이동 '''
    
    # 레코드 전체 삭제
    cur.execute("DELETE FROM detect")
    db.commit() # DB에 반영

    # LED와 센서 끄기(센서: 이벤트 삭제)
    GPIO.output(red_led, GPIO.LOW)
    GPIO.output(yellow_led, GPIO.LOW)
    GPIO.remove_event_detect(sensor['pin'])
    sensor['state'] = False

    # sensor 의 상태에 따라 home.html 의 구성이 바뀔 수 있도록 templateData 반환
    templateData = {'sensor': sensor}

    return render_template('home.html', **templateData)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
