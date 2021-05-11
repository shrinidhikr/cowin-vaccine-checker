# -*- coding: utf-8 -*-
"""
Created on Wed May  5 16:46:29 2021

@author: Shrinidhi KR
"""

from twilio.rest import Client
import requests
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'XXX'
auth_token = 'XXX'
client = Client(account_sid, auth_token)

contacts = [{'Name':'XYZ','pno':'whatsapp:+911234567890','pin':'560064','sent':False},{'Name':'ABC','pno':'whatsapp:+911234567890','pin':'577004','sent':False}]

@sched.scheduled_job('interval', minutes=720)
def scheduled_job():
    for x in contacts:
        x['sent'] = False


@sched.scheduled_job('interval', seconds=10)
def timed_job():
   
    for x in contacts:
        
        pin_code = x['pin']
        date = datetime.datetime.now().strftime("%d-%m-%Y")  
        
        url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode='+pin_code+'&date='+date
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
        r = requests.get(url,headers=headers)
        
        print("Status code: "+str(r.status_code))
        try:
            
            centers = r.json()
            
            sinfo = ''
            for i in range(len(centers['centers'])):
                clist = centers['centers'][i]['sessions']
                for j in range(len(clist)):
                    if(clist[j]['available_capacity']>0):
                        sinfo = sinfo + str(i+1) + '. ' + clist[j]['date'] + ' ' + centers['centers'][i]['name'] + ' Available Capacity - ' + str(clist[j]['available_capacity']) + '\n'
                
            print("Response string: \n"+sinfo)
            
            # this is the Twilio sandbox testing number
            from_whatsapp_number='whatsapp:+1234567890' 
            # replace this number with your own WhatsApp Messaging number
            to_whatsapp_number=x['pno']
            
            if(sinfo!='' and (not x['sent'])):
                message = client.messages.create(body= 'Hi '+x['Name']+' Vaccine centers are: \n' +sinfo, from_=from_whatsapp_number, to=to_whatsapp_number)
                x['sent'] = True
                print(message.sid)
        
        except Exception as e:
            print(r.text)
            print(e)
        
sched.start()