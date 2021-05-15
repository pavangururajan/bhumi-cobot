#!/usr/bin/python3
# -*- coding: utf8 -*-

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests


app = Flask(__name__)

CONTACT_RESOURCE = 'https://sheets.googleapis.com/v4/spreadsheets/1MLwVq41b1MHIONicCp3l6ip_AgSXJpjH6WxS0jY_sQA/values/Sheet1!A1:C200?key=AIzaSyATqNAWkr1Oh0H90z98KoV_yDg7om2CzMw'
RESOURCES = {}


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    msg = msg.strip().lower()

    reply_message = 'Please send your request in a format "I need X in Y". Eg: "I need hospital beds in Chennai"'

    # Create reply
    resp = MessagingResponse()

    if 'yes' in msg:
        reply_message = 'Stay Safe. Wear Masks.'
    elif 'no' in msg:
        reply_message = '''Please send your details in this format:\n
            Name:\n
            Contact No:\n
            City:
                '''
    elif 'name' in msg:
        pass
    else:
        pass

    resp.message(reply_message)

    return str(resp)


@app.route("/refresh", methods=['POST'])
def refresh_data():
    """Refresh contact data"""
    response = resources.get(CONTACT_RESOURCE)

    RESOURCE = {}

    if response.status_code == 200:
        for item in response.json()['values']:
            resource_type = item[0].lower().strip()
            resource_city = item[1].lower().strip()
            resource_contact = item[2]

            type_dict = RESOURCE.setdefault(resource_type, {})
            type_dict[resource_city] = resource_contact




if __name__ == "__main__":
    app.run(debug=True)
