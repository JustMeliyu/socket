# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, Response
from flask_socketio import SocketIO, emit, rooms, join_room
import json

app = Flask(__name__)
socketio = SocketIO()
socketio.init_app(app)


def ack(data):  # 服务端回调函数
    print(u'客户端已收到消息，回调参数为', data)  # 服务端回调函数的参数


@app.route('/')
def index():
    return render_template('test.html')


@app.route('/socket')
def test_emit():
    print(request.values)
    room = request.values.get('room')
    emit('alarms', namespace='/test', room=room, data=json.dumps(request.values))
    return Response(json.dumps({"status": "OK"}))


@socketio.on('connect', namespace='/test')
def connect():
    print("connect-"*4)
    print('----------')
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})


@socketio.on('join', namespace='/test')
def join(message):
    print("room", message)
    room = message.get('room')
    join_room(room, namespace='/test')


@socketio.on('client_event')
def client_msg(msg):
    print(msg)
    emit('server_response', {'data': msg['data']}, callback=ack)  # 指定服务端回调函数为ack，参数由客户端指定
    return 'server received data!'  # 客户端回调函数的参数


@socketio.on('connect_event')
def connected_msg(msg):
    print(u'客户端建立请求，信息为:', msg['data'])
    emit('server_response1', {'data': msg['data']})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5005, debug=True)
