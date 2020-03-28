from subprocess import call
from flask import Flask, render_template
from CTelescope import Telescope
from MessierObjects import CelestialObject
import datetime


t = Telescope(6, 16, 5, 13)

app = Flask(__name__)


@app.route('/')
def index():
    template_data = {'title': 'My Scope'}
    return render_template('index.html', **template_data)


@app.route('/iso/<iso>')
def set_iso(iso):
    global t
    t.set_iso(int(iso))
    template_data = {'title': 'My Scope', 'init': t.get_initialized()}
    return render_template('index.html', **template_data)


@app.route('/speed/<speed>')
def set_speed(speed):
    global t
    t.set_speed(int(speed))
    template_data = {'title': 'My Scope', 'init': t.get_initialized()}
    return render_template('index.html', **template_data)


@app.route('/exit')
def shutdown():
    call('sudo poweroff', shell=True)


@app.route('/initialize/<dt>')
def settime(dt):  # 45.801007399999996 15.1672683;2020-2-20 20:19:0
    global t
    params = dt.split(';')
    t.set_location(params[0])
    call('sudo date -s "'+params[1]+'"', shell=True)
    template_data = {'title': 'My Scope', 'init': t.get_initialized()}
    return render_template('index.html', **template_data)


@app.route('/locate/<param>')
def locate(param):
    # param ~ '72'
    global t
    template_data = {'title': 'Locating object', 'init': t.get_initialized()}

    p_obj_id = int(param)  # get object id

    # get datetime data
    dt = datetime.datetime.now()
    # print(dt)

    mo = CelestialObject(p_obj_id)
    template_data['Position'] = t.locate(mo, dt)

    return render_template('index.html', **template_data)


@app.route('/dir/<dir>')
def turn_scope(dir):
    global t
    template_data = {'title': 'My Scope', 'init': t.get_initialized()}

    if dir == 'left':
        t.turn_left()
    elif dir == 'right':
        t.turn_right()
    elif dir == 'up':
        t.turn_up()
    elif dir == 'down':
        t.turn_down()

    return render_template('index.html', **template_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context='adhoc')
