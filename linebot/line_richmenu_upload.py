from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('G4LPXeUwFFFHgmIlkFu0KXHLKJEgiyUxNahIUKusvhZYsi690q+mFfNpSVw4UHhxBU+/mbXwtWODQ6VGHsgoBzijvnO0tZFUKtBru0uS8/uWkIHd6RGTgvyuY8mULx/98FTXyhUde5VckdTko0xB2gdB04t89/1O/w1cDnyilFU=')

with open(r"C:\Users\Big data\Downloads\gogila.png", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-0ac1d2568ce7e8deab8ecd9bd298b289", "image/png", f)

import requests
headers = {"Authorization":"Bearer G4LPXeUwFFFHgmIlkFu0KXHLKJEgiyUxNahIUKusvhZYsi690q+mFfNpSVw4UHhxBU+/mbXwtWODQ6VGHsgoBzijvnO0tZFUKtBru0uS8/uWkIHd6RGTgvyuY8mULx/98FTXyhUde5VckdTko0xB2gdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-0ac1d2568ce7e8deab8ecd9bd298b289',
                       headers=headers)

print(req.text)