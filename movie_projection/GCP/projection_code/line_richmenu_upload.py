from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('G4LPXeUwFFFHgmIlkFu0KXHLKJEgiyUxNahIUKusvhZYsi690q+mFfNpSVw4UHhxBU+/mbXwtWODQ6VGHsgoBzijvnO0tZFUKtBru0uS8/uWkIHd6RGTgvyuY8mULx/98FTXyhUde5VckdTko0xB2gdB04t89/1O/w1cDnyilFU=')

with open(r"C:\Users\Big data\PycharmProjects\projection_moive37\projection_code\linebot_menu.png", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-15d179bdd4fac345f131ff002ed5d32e", "image/png", f)

import requests
headers = {"Authorization":"Bearer G4LPXeUwFFFHgmIlkFu0KXHLKJEgiyUxNahIUKusvhZYsi690q+mFfNpSVw4UHhxBU+/mbXwtWODQ6VGHsgoBzijvnO0tZFUKtBru0uS8/uWkIHd6RGTgvyuY8mULx/98FTXyhUde5VckdTko0xB2gdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-15d179bdd4fac345f131ff002ed5d32e',
                       headers=headers)

print(req.text)