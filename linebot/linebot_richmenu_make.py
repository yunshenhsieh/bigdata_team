import requests
import json

headers = {"Authorization":"Bearer G4LPXeUwFFFHgmIlkFu0KXHLKJEgiyUxNahIUKusvhZYsi690q+mFfNpSVw4UHhxBU+/mbXwtWODQ6VGHsgoBzijvnO0tZFUKtBru0uS8/uWkIHd6RGTgvyuY8mULx/98FTXyhUde5VckdTko0xB2gdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "six",
    "chatBarText": "RichMenu",
    "areas":[
        {
          "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
          "action": {"type": "message", "text": "分析預測毛彥森"}
        },
        {
          "bounds": {"x": 0, "y": 843, "width": 833, "height": 843},
          "action": {"type": "uri", "uri": "https://im.marieclaire.com.tw/m800c533h100b0/assets/mc/201906/5D02450A4DE5D1560429834.png"}
        },
        {
          "bounds": {"x": 833, "y": 0, "width": 833, "height": 843},
          "action": {"type": "message", "text": "linux沒壞姜怡甄"}
        },
        {
          "bounds": {"x": 833, "y": 843, "width": 833, "height": 843},
          "action": {"type": "message", "text": "mid down"}
        },
        {
          "bounds": {"x": 1666, "y": 0, "width": 833, "height": 843},
          "action": {"type": "message", "text": "修身養性莊雅捷"}
        },
        {
          "bounds": {"x": 1666, "y": 843, "width": 833, "height": 843},
          "action": {"type": "message", "text": "r down"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)