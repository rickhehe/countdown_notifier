#import appdaemon.plugins.hass.hassapi as hass

import re

import requests

# Use sys variable or secrests.yaml if you like
from config import username, password, apikey

URL_LOGIN = r'https://login.countdown.co.nz/accounts.login'
URL_PICKUP = r'https://shop.countdown.co.nz/api/v1/fulfilment/time-slots-summary'

HEADERS = {
    'x-requested-with':'OnlineShopping.WebApp'
}

PARAMS = {
    'loginID':username,
    'password':password,
    'ApiKey':apikey,
}


#class Countdown_notifier(hass.Hass):
class Countdown_notifier():

    def initialize(self):

        pass
        #try:
        #    self.run_every(
        #        self.stream,
        #        'now',
        #        60
        #    )
   
        #except Exception as e:

        #    self.send_email_to(
        #        message=e,
        #        title=f'Countdown_notifier Error'
        #    )

    @property
    def response(self, **kwargs):
 
        with requests.session() as session:

            session.post(
                URL_LOGIN,
                params=PARAMS,
            )
            
            r = session.get(
                URL_PICKUP,
                headers=HEADERS,
            )

        return r

    def stream(self):
        
        slots = self.response.json()['slots']
        if slots:
            for i in slots:
                yield (i['start'], i['end'], i['isExpress'])

#            self.send_email_to(
#                message='TBD',
#                title=f'Countdown Slots Available'
#            )

if __name__ == '__main__':
    
    try:
        x = Countdown_notifier()
        for i in x.stream():
            print(i)

    except Exception as e:
        print(e)
