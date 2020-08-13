from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# linebot參數設定
line_bot_api = LineBotApi('G4LPXeUwFFFHgmIlkFu0KXHLKJEgiyUxNahIUKusvhZYsi690q+mFfNpSVw4UHhxBU+/mbXwtWODQ6VGHsgoBzijvnO0tZFUKtBru0uS8/uWkIHd6RGTgvyuY8mULx/98FTXyhUde5VckdTko0xB2gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('81c080654026415b7968b9b1c4c6e8f3')

#搜集使用者記錄
@app.route("/callback", methods=['POST'])
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

# 跟使用者打招呼，說明linebot用途
@handler.add(MessageEvent, message=TextMessage)
def say_hello(event):
    if event.message.text=='Who are you':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='hello user,this is a pic collection.'))

# AWS套件匯入，設定環境
import boto3
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAR4NDUH53GWDLQFNM',
    aws_secret_access_key='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'
)

# 儲存使用者上傳的圖片，並上傳AWS s3
from linebot.models import ImageMessage
@handler.add(MessageEvent,message=ImageMessage)
def handle_image_message(event):
    # 請line_bot_api 把圖片從line抓回來，儲存到本地端
    # 圖片的名字以消息的id做命名
    # line_bot_api get message content line-bot-sdk
    message_content=line_bot_api.get_message_content(event.message.id)
    file_name =event.message.id + '.jpg'
    with open(file_name,'wb')as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    # 請line_bot_api 回覆用戶，說圖片已儲存。
    # line_bot_api reply TextSendMessage
    line_bot_api.reply_message(
        event.reply_token,
        [
         TextSendMessage(text='圖片已儲存，檔名為：' + file_name),
         TextSendMessage(text='I am so busy')
        ]
    )


    # 使用s3_client上傳至桶子內
    s3_client.upload_file(file_name, 'eb102', 'student3/'+ file_name)

if __name__ == "__main__":
    app.run(debug=True)