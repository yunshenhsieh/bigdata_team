# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

#
from linebot.exceptions import (
    InvalidSignatureError
)

# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import *

# 載入設定檔

import json
# secretFileContentJson=json.load(open("../line_secret_key",'r',encoding="utf-8"))
server_url="https://62b0ae3058cd.ap.ngrok.io"


# 設定Server啟用細節
app = Flask(__name__)

# 生成實體物件
line_bot_api = LineBotApi("G4LPXeUwFFFHgmIlkFu0KXHLKJEgiyUxNahIUKusvhZYsi690q+mFfNpSVw4UHhxBU+/mbXwtWODQ6VGHsgoBzijvnO0tZFUKtBru0uS8/uWkIHd6RGTgvyuY8mULx/98FTXyhUde5VckdTko0xB2gdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("81c080654026415b7968b9b1c4c6e8f3")

# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

'''

若收到圖片消息時，

先回覆用戶文字消息，並從Line上將照片拿回。

'''

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg=event.message.text
    if msg == '專題大大':
        message = TemplateSendMessage(
            alt_text='一則旋轉木馬按鈕訊息',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Number_1_in_green_rounded_square.svg/200px-Number_1_in_green_rounded_square.svg.png',
                        title='這是第一塊模板',
                        text='一個模板可以有三個按鈕',
                        actions=[
                            PostbackAction(
                                label='查理~~',
                                data='將這個訊息偷偷回傳給機器人'
                            ),
                            MessageAction(
                                label='wake up',
                                text='我知道這是1'
                            ),
                            URIAction(
                                label='查理專屬網頁',
                                uri='https://www.youtube.com/results?search_query=%E7%8D%A8%E8%A7%92%E7%8D%B8%E6%9F%A5%E7%90%86'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRuo7n2_HNSFuT3T7Z9PUZmn1SDM6G6-iXfRC3FxdGTj7X1Wr0RzA',
                        title='這是第二塊模板',
                        text='副標題可以自己改',
                        actions=[
                            PostbackAction(
                                label='怡甄，別再弄壞linux了。',
                                data='這是ID=2'
                            ),
                            MessageAction(
                                label='雖然我會修。',
                                text='我知道這是2'
                            ),
                            URIAction(
                                label='進入2的網頁',
                                uri='https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Number_2_in_light_blue_rounded_square.svg/200px-Number_2_in_light_blue_rounded_square.svg.png'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Number_3_in_yellow_rounded_square.svg/200px-Number_3_in_yellow_rounded_square.svg.png',
                        title='這是第三個模塊',
                        text='最多可以放十個',
                        actions=[
                            PostbackAction(
                                label='我做出來了。',
                                data='這是ID=3'
                            ),
                            MessageAction(
                                label='雅捷別生氣。',
                                text='我知道這是3'
                            ),
                            URIAction(
                                label='uri2',
                                uri='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Number_3_in_yellow_rounded_square.svg/200px-Number_3_in_yellow_rounded_square.svg.png'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)


'''

啟動Server

'''
if __name__ == "__main__":
    app.run(host='0.0.0.0')