__author__ = 'vyshakh.babji'

import time
from rcsdk import RCSDK
from threading import Thread
from time import sleep
from rcsdk.subscription import EVENTS

#Instantiating the SDK
RC_SERVER_PRODUCTION = 'https://platform.ringcentral.com'
RC_SERVER_SANDBOX = 'https://platform.devtest.ringcentral.com'
YOUR_APPKEY = 'E0_nOAfbR7GkteYbDv93oA'
YOUR_APPSECRET = 'UelNnk-1QYK0rHyvjJJ9yQx3Yl6vj3RvGmb0G2SH6ePw'
YOUR_PHONENUMBER= '15856234138'
YOUR_EXTENSION=''
YOUR_PASSWORD= 'P@ssw0rd'
sdk = RCSDK(YOUR_APPKEY, YOUR_APPSECRET , RC_SERVER_SANDBOX)


#Getting the Platform Singleton
platform = sdk.get_platform()

#Login
platform.authorize(YOUR_PHONENUMBER, YOUR_EXTENSION, YOUR_PASSWORD)

#Determining Authn Status
platform.is_authorized()

#Manual Access Token Refresh
platform.refresh()

#Account and Extension Information
response = platform.get('/account/~/extension/~')
user = response.get_json(True)
user_id = str(user.id)
print('User loaded ' + user.name + ' (' + user_id + ')')
print('User Information : ' + str(response.get_body()))

#Call Log
response = platform.get('/account/~/extension/~/call-log')
print('Call-Log Information : ' + str(response.get_body()))


#Active Calls
response = platform.get('/account/~/extension/~/active-calls')
print('Active-Call-Log Information : ' + str(response.get_body()))


#Message Store
response = platform.get('/account/~/extension/~/message-store')
print('Message store Information : ' + str(response.get_body()))



#Send SMS
to_Number = '16197619503'
from_Number =  '15856234138'
message = "Hi, This is the test message"
sms_body = {"to":[{"phoneNumber":to_Number}],"from":{"phoneNumber":from_Number},"text":message}

response = platform.post(url='/account/~/extension/~/sms',body=sms_body)
print('SMS Information: ' + str(response.get_body()))

#RingOut: Making Calls
# to_Number = '16197619503'
# from_Number =  '16505154891'
# caller_Id = '15856234138'
# ringout_body = {
#   "to": {"phoneNumber": to_Number},
#   "from": {"phoneNumber": from_Number},
#   "callerId": {"phoneNumber": caller_Id},
#   "playPrompt": "true"
# }
#
#
# response = platform.post(url='/account/~/extension/~/ringout',body=ringout_body)
# print('RingOut Information: ' + str(response.get_body()))
# ringout = response.get_json(True)


#RingOut: Disconnect Calls
# ringout_Id = str(ringout.id);
# print ringout_Id
# time.sleep(5)
#
# response = platform.delete(url = '/account/~/extension/~/ringout/'+ringout_Id)
# print('RingOut Delete Information : ' + str(response.get_status()))


#Presence
response = platform.get(url = '/account/~/extension/~/presence')
print('Presence Information : ' + str(response.get_body()))


#Subscription
res = platform.get( url= '/account/~/extension/~')
print('User loaded ' + res.get_json().name)



def on_message(msg):
    print(msg)

def pubnub():
    s = sdk.get_subscription()
    #s.add_events(['/account/~/extension/~/message-store','/account/~/extension/~/presence'])
    s.add_events(['/restapi/v1.0/account/~/extension/~/presence?detailedTelephonyState=true'])
    s.on(EVENTS['notification'], on_message)
    s.register()
    while True:
        sleep(0.1)

try:
    try:
        import Pubnub
        t = Thread(target=pubnub)
        t.start()
    except ImportError as e:
        print("No Pubnub SDK, skipping Pubnub test")
except KeyboardInterrupt:
    pass