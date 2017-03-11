# -*- coding: utf-8 -*-
# from __future__ import absolute_import

from flask import Flask, render_template
from flask_sockets import Sockets

from moves import press_keys, initialize_keyboard

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/api')
def echo_socket(ws):
    print("Going to start websocket")
    initialize_keyboard()
    while not ws.closed:
        print("Running...")
        message = ws.receive()
        if message is not None:
            press_keys(message)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
