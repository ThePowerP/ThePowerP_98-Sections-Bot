import requests
import json
import twitter
import coloredlogs
import logging
import aiohttp
import time
from util import Utility

log = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="[%(asctime)s] %(message)s", datefmt="%I:%M:%S")

with open('configuracion.json') as f:
    config = json.load(f)

delay = config['delay']

while True:
    with open('Cache/sections.json', 'r')as file:
        old = json.load(file)
    r = requests.get('https://fn-api.com/api/shop_categories')
    # print(r)
    response = r.json()
    if response != old:
        a = ''
        for gang in response['shopCategories']:
            categoria = gang['sectionName']
            cantidad = gang['quantity']
            a += f'\n{categoria} x {cantidad}'
        try:
            twitterAPI = twitter.Api(
                consumer_key=config['twitterAPIKey'],
                consumer_secret=config['twitterAPISecret'],
                access_token_key=config['twitterAccessToken'],
                access_token_secret=config['twitterAccessSecret'],
            )
        except Exception as e:
            log.critical(f'Error al autentificar con twitter, {e}.')
        body = a
        try:
            twitterAPI.PostUpdate(body)
        except Exception as e:
            log.critical(f'Error al Twittear las secciones, {e}')
    with open('Cache/sections.json', 'w')as file:
        json.dump(response, file, indent=3)
    time.sleep(delay)
