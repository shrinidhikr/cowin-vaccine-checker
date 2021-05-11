# -*- coding: utf-8 -*-
"""
Created on Thu May  6 20:38:41 2021

@author: Shrinidhi KR
"""

from twilio.rest import Client

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
account_sid = 'XXX'
auth_token = 'XXX'
client = Client(account_sid, auth_token)

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+1234567890' 
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:+911234567890'

client.messages.create(body='Ahoy, world!',
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)