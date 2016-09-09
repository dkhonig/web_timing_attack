#!/usr/bin/env python

import hashlib, json
from flask import Flask, abort
app = Flask(__name__)

KEY = 'qp079hpzsso7ynei0w35'

def verify_sig(event_id):
    input = event_id + KEY
    h = hashlib.sha1(input.encode())
    return str(h.hexdigest())[0:8]

@app.route("/")
def index():
    return "Timing attack server running.. <br/><br/>" \
    "<u>Test Parameters</u><br/> EventID: 19295929 <br/> Signature: 2802b7a0" \
    "<br/> <a href='/events/19295929/2802b7a0/'>http://localhost:5000/events/19295929/2802b7a0/</a>"

@app.route("/events/<event_id>/<signature>/")
def events(event_id, signature):
    if not event_id or not signature:
        abort(404)

    if signature == verify_sig(event_id):
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        abort(404)

if __name__ == "__main__":
    app.run()