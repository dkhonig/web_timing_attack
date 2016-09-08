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
    return "Timing attack server running.. \n Try testing eventid: 19295929 signature: 2802b7a0"

@app.route("/events/<event_id>/<signature>/")
def events(event_id, signature):
    if not event_id or not signature:
        abort(404)

    if signature == verify_sig(event_id):
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        abort(404)

if __name__ == "__main__":
    #print hash_signature('19295929')
    app.run()