import appdaemon.plugins.hass.hassapi as hass

import re

import requests

# Use sys variable or secrests.yaml if you like

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


class Countdown_notifier(hass.Hass):

    def initialize(self):
        self.log(f'{__name__} is now live.')
        try:
            self.run_every(
                self.stream,
                'now',
                30
            )
        except Exception as e:
            self.send_email_to(
                message=e,
                title=f'Countdown_notifier Error'
            )

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

    def send_email_to(self, message, title=''):
        
        self.call_service(
            'notify/send_email_to_rick_notifier',
            message=message,
            title=title,
        )
        
    def stream(self, kwargs):
        
        slots = self.response.json()['slots']
        if slots:
            
            x =  [
                f'start: {i["start"]}, end: {i["end"]}, express: {i["isExpress"]}'
                for i in slots
            ]
            x = '\n'.join(x)

            self.send_email_to(
                message=x,
                title=f'Countdown Slots Available'
            )
