import threading
from subprocess import call
from flask import Flask, render_template, jsonify, Response, request
from flask_socketio import SocketIO

from CTelescope import Telescope
# from CCamera import Camera

from sky_object_data import get_objects, find_objects
from LocationInfo import LocationInfo
from TargetInfo import TargetInfo



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


t = Telescope(6, 13, 5, 19)
# c = Camera()
li = LocationInfo()
ti = TargetInfo()  # last target (for tracking)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/filter_data/', methods=['GET'])
def filter_data():

    params = request.args.to_dict()
    # params['m'] = True if params['m'] == 'true' else False
    return jsonify(get_objects(t=params['t'] if 't' in params else '', c=params['c'] if 'c' in params else '', m=True if 'm' in params and params['m'] == 'true' else False, li=li))


@app.route('/search/', methods=['GET'])
def search():

    params = request.args.to_dict()

    return jsonify(find_objects(params['q']))  #, params['t']))


@app.route('/steps/<steps>')
def set_steps(steps):

    t.set_manual_steps(int(steps))
    return jsonify({
        "message": 'Steps set to ' + steps,
    })


@app.route('/initialize/<dt>')
def set_time_and_location(dt):  # 45.801007399999996 15.1672683;2020-2-20 20:19:0

    params = dt.split(';')
    print(params)

    # set location
    li.set_location(params[0])

    # set system time
    call('sudo date -s "'+params[1]+'"', shell=True)

    # start camera
    # if not c.streaming:
    #     c.start_streaming()

    return jsonify({'message': 'Location & time set: ' + dt})


@app.route('/lookingAt/<param>')
def looking_at(param):

    ti.set_target(param)

    return jsonify({
        "message": 'Looking at ' + t.looking_at(ti, li),
    })


@app.route('/locate/<param>')
def locate(param):

    ti.set_target(param)

    return jsonify({
        "message": 'Tracking ' + t.locate(ti, li),
    })


@app.route('/set_altitude/<alt>')
def set_altitude(alt):

    t.turn_to_altitude(int(alt))
    return jsonify({
        "message": 'Set altitude: ' + alt,
    })


@app.route('/set_azimuth/<az>')
def set_azimuth(az):

    t.turn_to_azimuth(int(az))
    return jsonify({
        "message": 'Set azimuth: ' + az,
    })


@app.route('/startTracking')
def start_tracking():

    print('started tracking:', ti.get_obj())
    t1 = threading.Thread(target=t.start_tracking, args=[ti, li])
    t1.start()
    t1.join()
    print('stoped tracking:', ti.get_obj())
    return 'Started tracking'


@app.route('/stopTracking')
def stop_tracking():

    t.stop_tracking()
    return 'Stopped tracking'


# manual corrections
@app.route('/dir/<direction>')
def turn_scope(direction):

    if direction == 'left':
        t.turn_left(t.manual_steps)
    elif direction == 'right':
        t.turn_right(t.manual_steps)
    elif direction == 'up':
        t.turn_up(t.manual_steps)
    elif direction == 'down':
        t.turn_down(t.manual_steps)

    return jsonify({
        "message": 'Turned ' + direction,
    })

@app.route('/start_turning/<dir>')
def start_turning(dir):
    if dir == 'left':
        t.start_turning_left()
    elif dir == 'right':
        t.start_turning_right()
    elif dir == 'up':
        t.start_turning_up()
    elif dir == 'down':
        t.start_turning_down()

    return jsonify({
        "message": 'Startet turning ' + dir,
    })
    

@app.route('/stop_turning/<dir>')
def stop_turning(dir):
    if dir == 'left':
        t.stop_turning_left()
    elif dir == 'right':
        t.stop_turning_right()
    elif dir == 'up':
        t.stop_turning_up()
    elif dir == 'down':
        t.stop_turning_down()

    return jsonify({
        "message": 'Stoped turning ' + dir,
    })

# reset position
@app.route('/resetPosition')
def reset_position():
    t.reset_position()
    return jsonify({
        "message": "Position reset. Level the scope and turn it North.",
    })


# def gen():

#     while True:
#         frame = c.get_frame()
#         if frame is not None:
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/take_picture')
# def take_picture():  # tale zna crknit, če je kamera ugasnjena

#     img = c.get_picture()
#     #print('Took image:', img)
#     return jsonify({
#         "message": "Image saved to: <a href='static/pictures/"+img+"' target='_blank'>"+img+"</a>",
#         "src": "static/pictures/"+img,
#     })


# @app.route('/video_feed')
# def video_feed():

#     return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/exit')
def shutdown():

    # c.quit() # quit camera
    call('sudo poweroff', shell=True)


# @app.route('/set_iso/<iso>')
# def set_iso(iso):

#     c.set_iso(int(iso))
#     return jsonify({"message": "ISO set to: " + iso, })


# @app.route('/set_exp/<exp>')
# def set_exp(exp):
#
#     c.set_exp(int(exp))
#     return jsonify({"message": "Exposure set to: " + exp, })


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=False, port=80, ssl_context=('telescope.crt', 'telescope.key'))
    socketio.run(app=app, host='0.0.0.0', debug=False, port=80, ssl_context=('telescope.crt', 'telescope.key'))
