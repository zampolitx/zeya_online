#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests

req = requests.get('https://ok.ru/gorodzeya')
soup = BeautifulSoup(req.text, "lxml")
obyavleniya=soup.prettify()
print(soup.find(id='music_layer_wrapper'))
'''<div class="hook delete-stub" id="hook_Block_Rfa34439358659d8f094482d7"></div>'''