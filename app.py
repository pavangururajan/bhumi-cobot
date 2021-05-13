#!/usr/bin/python3
# -*- coding: utf8 -*-

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    msg = msg.strip()

    reply_message = 'Please send your request in a format "I need X in Y". Eg: "I need hospital beds in Chennai"'

    # Create reply
    resp = MessagingResponse()
    resp.message(reply_message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
