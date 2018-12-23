import logging
import urllib

import requests

from lxml import html


CHROME_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '\
            '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'


class MissingProductError(Exception):
    pass


class InvalidTelegramConnError(Exception):
    pass


def get_site_elements(url):
    ''' Get the ElementTree '''
    r = requests.get(url, headers={'user-agent': CHROME_UA})
    if not r:
        logging.error('Could not fetch: {}. Status: {}'.format(url,
                                                               r.status_code))
        raise MissingProductError

    tree = html.fromstring(r.content)
    return tree


def send_tg_message(message, bot_token, chat_id):
    ''' Send given message to chat '''
    base_url = 'https://api.telegram.org'
    url = base_url + '/bot{}/sendMessage'.format(bot_token)
    payload = {'chat_id': chat_id, 'text': message}
    r = requests.get(url, params=payload)
    if not r:
        logging.error('Could not send a message to chat: {}. '\
                      'Status: {}'.format(chat_id, r.status_code))
        raise InvalidTelegramConnError

'''
def get_chat_id():
    token = TELEGRAM['botToken']
    r = requests.get(f'https://api.telegram.org/bot{token}/getUpdates')
    content = r.json()
    for i in content['result']:
        if i['message']['chat']['username'] == TELEGRAM.get('user'):
            id = i['message']['chat']['id']
            print(f'Chat id: {id}')
'''
