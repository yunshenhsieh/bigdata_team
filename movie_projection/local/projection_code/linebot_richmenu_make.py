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
          "action": {"type": "message", "text": "英文電影推薦"}
        },
        {
          "bounds": {"x": 0, "y": 843, "width": 833, "height": 843},
          "action": {"type": "message", "text": "圖像推薦"}
        },
        {
          "bounds": {"x": 833, "y": 0, "width": 833, "height": 843},
          "action": {"type": "message", "text": "中文電影推薦"}
        },
        {
          "bounds": {"x": 833, "y": 843, "width": 833, "height": 843},
          "action": {"type": "message", "text": "輿論評估"}
        },
        {
          "bounds": {"x": 1666, "y": 0, "width": 833, "height": 843},
          "action": {"type": "message", "text": "喜好推薦"}
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