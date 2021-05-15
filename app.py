#!/usr/bin/python3
# -*- coding: utf8 -*-

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from sheet_update import read_data, write_data


app = Flask(__name__)

RESOURCES = {}


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    global RESOURCES
    if not RESOURCES:
        RESOURCES = refresh_data()

    #print("Resources ===")
    #print(RESOURCES)
    #print("Resources ===")

    # Fetch the message
    msg = request.form.get('Body')

    msg = msg.strip().lower()

    reply_message = 'Please send your request in a format "I need X in Y". Eg: "I need hospital beds in Chennai"'

    # Create reply
    resp = MessagingResponse()
    #print("Message => %s" % msg)

    if 'yes' in msg:
        reply_message = 'Stay Safe. Wear Masks.'
    elif 'no' in msg:
        reply_message = '''Please send your details in this format so that we can contact you when it is available:\nName:\nContact No:\nCity:'''
    elif 'name' in msg:
        #print("Name => %s" % msg)
        write_data(msg)
        reply_message = 'We have noted down your contact. We will reach you when we get any information'
    elif 'need' in msg or 'want' in msg:
        #print("Need => %s" % msg)
        words = msg.split()
        #print("Words: %s" % words)
        no_resource = True
        resource_dict = {}
        for each_word in words:
            if each_word in RESOURCES:
                resource_dict = RESOURCES[each_word]
        if resource_dict:
            for each_word in reversed(words):
                if each_word in resource_dict:
                    reply_message = resource_dict[each_word]
                    reply_message = "%s\n%s" % (reply_message, 'Please type "Yes" if it is useful, "No" if it is not')
                    no_resource = False
                    break
        if no_resource:
            reply_message = '''We couldn't find any information. Please send your details in this format so that we can contact you when it is available:\nName:\nContact No:\nCity:'''
    else:
        pass
    #print("Reply => %s" % reply_message)

    resp.message(reply_message)

    return str(resp)


@app.route("/refresh", methods=['POST'])
def refresh_data():
    """Refresh contact data"""
    data = read_data()
    global RESOURCES

    RESOURCE = {}

    if data:
        for item in data[1:]:
            resource_type = item[0].lower().strip()
            resource_city = item[1].lower().strip()
            resource_contact = item[2]

            type_dict = RESOURCE.setdefault(resource_type, {})
            type_dict[resource_city] = resource_contact
    RESOURCES = RESOURCE

    return RESOURCE


if __name__ == "__main__":
    RESOURCES = refresh_data()
    app.run(debug=True)
