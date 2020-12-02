from flask import Flask, request
from flask import render_template

app = Flask(__name__)

led_pin = {
    'bcm': 23,
    'state': False
}

result = {
    'from': 1006,
    'to': 1030
}

@app.route('/')
def home():
    templateData = {'sensor': led_pin}

    return render_template('home.html', **templateData)

@app.route('/sensor/<action>')
def sensor_on_off(action):

    if action == "on":
        led_pin['state'] = True

    if action == "off":
        led_pin['state'] = False

    templateData = {'sensor': led_pin}

    return render_template('home.html', **templateData)

@app.route('/result')
def show_result():
    templateData = {'result': result}

    return render_template('result.html', **templateData)

@app.route('/play')
def play_image():
    templateData = {'result': result}
    
    return render_template('play.html', **templateData)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
