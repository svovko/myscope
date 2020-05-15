from subprocess import call
from flask import Flask, render_template, jsonify, Response
from CTelescope import Telescope
from sky_object_data import stars, messier_objects
from co import CelestialObject
from CCamera import Camera
import datetime


app = Flask(__name__)

t = Telescope(6, 16, 5, 13)
c = Camera()
template_data = {'title': 'My Scope', 'stars': stars, 'mo': messier_objects}


@app.route('/')
def index():

    return render_template('index.html', **template_data)


@app.route('/steps/<steps>')
def set_steps(steps):

    t.set_manual_steps(int(steps))
    return jsonify({
        "message": 'Steps set to ' + steps,
    })


@app.route('/initialize/<dt>')
def settime(dt):  # 45.801007399999996 15.1672683;2020-2-20 20:19:0

    params = dt.split(';')
    t.set_location(params[0])
    call('sudo date -s "'+params[1]+'"', shell=True)

    return jsonify({'message': 'Location & time set: ' + dt})


@app.route('/lookingAt/<param>')
def looking_at(param):
    # param ~ '72'

    p_obj_id = int(param)  # get object id

    # get datetime data
    dt = datetime.datetime.now()

    mo = CelestialObject(p_obj_id)

    return jsonify({
        "message": 'Looking at ' + t.looking_at(mo, dt),
    })


@app.route('/locate/<param>')
def locate(param):
    # param ~ '72'

    p_obj_id = int(param)  # get object id

    # get datetime data
    dt = datetime.datetime.now()

    mo = CelestialObject(p_obj_id)

    return jsonify({
        "message":  'Located ' + t.locate(mo, dt),
    })


@app.route('/dir/<dir>')
def turn_scope(dir):

    if dir == 'left':
        t.turn_left()
    elif dir == 'right':
        t.turn_right()
    elif dir == 'up':
        t.turn_up()
    elif dir == 'down':
        t.turn_down()

    return jsonify({
        "message": 'Turned ' + dir,
    })


def gen():

    while True:
        frame = c.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/take_picture')
def take_picture():  # tale zna crknit, če je kamera ugasnjena

    img = c.get_picture()
    print('Took image:', img)
    return jsonify({
        "message": "Image saved to: <a href='static/pictures/"+img+"' target='_blank'>"+img+"</a>",
    })


@app.route('/video_feed')
def video_feed():

    # c.start_streaming()
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/start_camera')
def start_camera():

    c.start_streaming()
    return jsonify({"message": "Camera started", })


@app.route('/stop_camera')
def stop_camera():

    c.stop_streaming()
    return jsonify({"message": "Camera stopped", })


@app.route('/exit')
def shutdown():

    c.quit()
    call('sudo poweroff', shell=True)


@app.route('/set_iso/<iso>')
def set_iso(iso):

    c.set_iso(int(iso))
    return jsonify({"message": "ISO set to: " + iso, })


@app.route('/set_exp/<exp>')
def set_exp(exp):

    c.set_exp(int(exp))
    return jsonify({"message": "Exposure set to: " + exp, })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context='adhoc')
