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


# secretFileContentJson=json.load(open("../line_secret_key",'r',encoding="utf-8"))
# server_url="https://6a58dd9c8683.ap.ngrok.io"

# 設定Server啟用細節
app = Flask(__name__)
GCP_IP='104.199.132.135'
imdb_post_path='https://storage.googleapis.com/projection_post/imdb_post/'
yahoo_post_path='https://storage.googleapis.com/projection_post/yahoo_post/'
# 生成實體物件
line_bot_api = LineBotApi("G4LPXeUwFFFHgmIlkFu0KXHLKJEgiyUxNahIUKusvhZYsi690q+mFfNpSVw4UHhxBU+/mbXwtWODQ6VGHsgoBzijvnO0tZFUKtBru0uS8/uWkIHd6RGTgvyuY8mULx/98FTXyhUde5VckdTko0xB2gdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("81c080654026415b7968b9b1c4c6e8f3")

from pymongo import MongoClient
import json
# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    kaf_producer(body)
    try:
        if 'tt' in json.loads(body)['events'][0]['postback']['data'].split(':')[1]:
            userId=json.loads(body)['events'][0]['source']['userId']
            imdbId=json.loads(body)['events'][0]['postback']['data'].split(':')[1]
            kaf_producer_like(userId,imdbId)
    except:
        print('no postback')

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


import pandas as pd
from keras.preprocessing import image
from keras.models import load_model
import numpy as np
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
    img_path='./'+file_name

    # 將圖片轉為待測數據
    path = './train_photo.csv'
    f = open(path)
    train = pd.read_csv(f)

    model = load_model('movies_post.h5')

    # 開啟圖片路徑進行預測，與前面步驟相同
    imagelist = [img_path]
    for file in imagelist:
        photo_recommend_list = []
        try:
            img = image.load_img(file, target_size=(400, 400, 3))
            img = image.img_to_array(img)
            img = img / 255

            classes = np.array(train.columns[2:])  # 分類
            proba = model.predict(img.reshape(1, 400, 400, 3))  # 分數
            top_3 = np.argsort(proba[0])[:-4:-1]  # [:-4:-1]選出前3高的分數

            for i in range(3):
                print("{}".format(classes[top_3[i]]) + " ({:.3})".format(proba[0][top_3[i]]))
                photo_recommend_list+=[name_tuple for name_tuple in (sql_animation(classes[top_3[i]]))]

        except OSError as e:
            pass
            print('oserror')
    message = TemplateSendMessage(
        alt_text='圖像推薦結果',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=imdb_post_path + '{}.jpg'.format(photo_recommend_list[0][1]),
                    title='{}'.format(photo_recommend_list[0][0]),
                    text='圖像推薦:1',
                    actions=[
                        PostbackAction(
                            label='喜歡這部電影',
                            data='喜歡電影的id:{}'.format(photo_recommend_list[0][1])
                        ),
                        MessageAction(
                            label='相關推薦',
                            text='外國電影{}的相關推薦'.format(photo_recommend_list[0][0])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=imdb_post_path + '{}.jpg'.format(photo_recommend_list[1][1]),
                    title='{}'.format(photo_recommend_list[1][0]),
                    text='圖像推薦:2',
                    actions=[
                        PostbackAction(
                            label='喜歡這部電影',
                            data='喜歡電影的id:{}'.format(photo_recommend_list[1][1])
                        ),
                        MessageAction(
                            label='相關推薦',
                            text='外國電影{}的相關推薦'.format(photo_recommend_list[1][0])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=imdb_post_path + '{}.jpg'.format(photo_recommend_list[2][1]),
                    title='{}'.format(photo_recommend_list[2][0]),
                    text='圖像推薦:3',
                    actions=[
                        PostbackAction(
                            label='喜歡這部電影',
                            data='喜歡電影的id:{}'.format(photo_recommend_list[2][1])
                        ),
                        MessageAction(
                            label='相關推薦',
                            text='外國電影{}的相關推薦'.format(photo_recommend_list[2][0])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=imdb_post_path + '{}.jpg'.format(photo_recommend_list[3][1]),
                    title='{}'.format(photo_recommend_list[3][0]),
                    text='圖像推薦:4',
                    actions=[
                        PostbackAction(
                            label='喜歡這部電影',
                            data='喜歡電影的id:{}'.format(photo_recommend_list[3][1])
                        ),
                        MessageAction(
                            label='相關推薦',
                            text='外國電影{}的相關推薦'.format(photo_recommend_list[3][0])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=imdb_post_path + '{}.jpg'.format(photo_recommend_list[4][1]),
                    title='{}'.format(photo_recommend_list[4][0]),
                    text='圖像推薦:5',
                    actions=[
                        PostbackAction(
                            label='喜歡這部電影',
                            data='喜歡電影的id:{}'.format(photo_recommend_list[4][1])
                        ),
                        MessageAction(
                            label='相關推薦',
                            text='外國電影{}的相關推薦'.format(photo_recommend_list[4][0])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=imdb_post_path + '{}.jpg'.format(photo_recommend_list[5][1]),
                    title='{}'.format(photo_recommend_list[5][0]),
                    text='圖像推薦:6',
                    actions=[
                        PostbackAction(
                            label='喜歡這部電影',
                            data='喜歡電影的id:{}'.format(photo_recommend_list[5][1])
                        ),
                        MessageAction(
                            label='相關推薦',
                            text='外國電影{}的相關推薦'.format(photo_recommend_list[5][0])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=imdb_post_path + '{}.jpg'.format(photo_recommend_list[6][1]),
                    title='{}'.format(photo_recommend_list[6][0]),
                    text='圖像推薦:7',
                    actions=[
                        PostbackAction(
                            label='喜歡這部電影',
                            data='喜歡電影的id:{}'.format(photo_recommend_list[6][1])
                        ),
                        MessageAction(
                            label='相關推薦',
                            text='外國電影{}的相關推薦'.format(photo_recommend_list[6][0])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=imdb_post_path + '{}.jpg'.format(photo_recommend_list[7][1]),
                    title='{}'.format(photo_recommend_list[7][0]),
                    text='圖像推薦:8',
                    actions=[
                        PostbackAction(
                            label='喜歡這部電影',
                            data='喜歡電影的id:{}'.format(photo_recommend_list[7][1])
                        ),
                        MessageAction(
                            label='相關推薦',
                            text='外國電影{}的相關推薦'.format(photo_recommend_list[7][0])
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=imdb_post_path + '{}.jpg'.format(photo_recommend_list[8][1]),
                    title='{}'.format(photo_recommend_list[8][0]),
                    text='圖像推薦:9',
                    actions=[
                        PostbackAction(
                            label='喜歡這部電影',
                            data='喜歡電影的id:{}'.format(photo_recommend_list[8][1])
                        ),
                        MessageAction(
                            label='相關推薦',
                            text='外國電影{}的相關推薦'.format(photo_recommend_list[8][0])
                        )
                    ]
                ),
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

'''
若收到圖片消息時，
先回覆用戶文字消息，並從Line上將照片拿回。
'''
import random,redis
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg=event.message.text
    if msg == '英文電影推薦':
        movie_name=mongo_imdb()
        message = TemplateSendMessage(
            alt_text='英文電影推薦結果',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path+'{}.jpg'.format(movie_name[0]['_id']),
                        title='{}'.format(movie_name[0]['IMDB電影名']),
                        text='英文電影推薦:1',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[0]['_id'])
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[0]['IMDB電影名'])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(movie_name[1]['_id']),
                        title='{}'.format(movie_name[1]['IMDB電影名']),
                        text='英文電影推薦:2',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[1]['_id'])
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[1]['IMDB電影名'])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(movie_name[2]['_id']),
                        title='{}'.format(movie_name[2]['IMDB電影名']),
                        text='英文電影推薦:3',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[2]['_id'])
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[2]['IMDB電影名'])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(movie_name[3]['_id']),
                        title='{}'.format(movie_name[3]['IMDB電影名']),
                        text='英文電影推薦:4',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[3]['_id'])
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[3]['IMDB電影名'])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(movie_name[4]['_id']),
                        title='{}'.format(movie_name[4]['IMDB電影名']),
                        text='英文電影推薦:5',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[4]['_id'])
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[4]['IMDB電影名'])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(movie_name[5]['_id']),
                        title='{}'.format(movie_name[5]['IMDB電影名']),
                        text='英文電影推薦:6',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[5]['_id'])
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[5]['IMDB電影名'])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(movie_name[6]['_id']),
                        title='{}'.format(movie_name[6]['IMDB電影名']),
                        text='英文電影推薦:7',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[6]['_id'])
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[6]['IMDB電影名'])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(movie_name[7]['_id']),
                        title='{}'.format(movie_name[7]['IMDB電影名']),
                        text='英文電影推薦:8',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[7]['_id'])
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[7]['IMDB電影名'])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(movie_name[8]['_id']),
                        title='{}'.format(movie_name[8]['IMDB電影名']),
                        text='英文電影推薦:9',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[8]['_id'])
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[8]['IMDB電影名'])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(movie_name[9]['_id']),
                        title='{}'.format(movie_name[9]['IMDB電影名']),
                        text='英文電影推薦:10',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[9]['_id'])
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[9]['IMDB電影名'])
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)

    elif msg == '輿論評估':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='格式為「輿論評估：電影名稱」'))

    elif '輿論評估：' in msg:
        msg_comment=msg.replace(':','\n').replace('：','\n').split('\n')
        con = MongoClient('mongodb://'+ GCP_IP +':27017/')
        db = con.Movie_project
        dis = db.movie_similarity.count({'電影中文名': "{}".format(msg_comment[1])})
        print(dis)
        if dis != 0:
            good,bad=comment_use(msg_comment[1])
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=msg_comment[1]+'的好評有'+ str(good) +'篇'),
                    TextSendMessage(text=msg_comment[1]+'的負評有' + str(bad) + '篇')
                ]
            )
        else:
            line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='沒有這部電影')
            )
    elif msg == '圖像推薦':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請上傳「一張圖片」或「直接照張像」'))

    elif msg == '中文電影推薦':
        con = MongoClient('mongodb://'+ GCP_IP +':27017/')
        db = con.Movie_project
        dis = db.movie_similarity.find()
        dis=list(dis)
        dis=[(di['電影中文名'],di['_id']) for di in dis]
        movie_name = random.sample(dis, k=10)

        message = TemplateSendMessage(
            alt_text='中文電影推薦結果',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path+'{}.jpg'.format(movie_name[0][1]),
                        title='{}'.format(movie_name[0][0]),
                        text='中文電影推薦:1',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[0][1])
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[0][0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[0][0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(movie_name[1][1]),
                        title='{}'.format(movie_name[1][0]),
                        text='中文電影推薦:2',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[1][1])
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[1][0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[1][0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(movie_name[2][1]),
                        title='{}'.format(movie_name[2][0]),
                        text='中文電影推薦:3',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[2][1])
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[2][0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[2][0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(movie_name[3][1]),
                        title='{}'.format(movie_name[3][0]),
                        text='中文電影推薦:4',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[3][1])
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[3][0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[3][0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(movie_name[4][1]),
                        title='{}'.format(movie_name[4][0]),
                        text='中文電影推薦:5',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[4][1])
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[4][0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[4][0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(movie_name[5][1]),
                        title='{}'.format(movie_name[5][0]),
                        text='中文電影推薦:6',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[5][1])
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[5][0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[5][0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(movie_name[6][1]),
                        title='{}'.format(movie_name[6][0]),
                        text='中文電影推薦:7',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[6][1])
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[6][0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[6][0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(movie_name[7][1]),
                        title='{}'.format(movie_name[7][0]),
                        text='中文電影推薦:8',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[7][1])
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[7][0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[7][0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(movie_name[8][1]),
                        title='{}'.format(movie_name[8][0]),
                        text='中文電影推薦:9',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[8][1])
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[8][0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[8][0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(movie_name[9][1]),
                        title='{}'.format(movie_name[9][0]),
                        text='中文電影推薦:10',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(movie_name[9][1])
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[9][0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[9][0])
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)

    elif ('相關推薦' and '中文') in msg:
        con = MongoClient('mongodb://'+ GCP_IP +':27017/')
        db = con.Movie_project
        dis = db.movie_similarity.find({'電影中文名':"{}".format(msg.split('的相關推薦')[0].split('中文電影')[1])})
        movie_name = list(dis[0]['其他電影相似度'].keys())[:]
        message = TemplateSendMessage(
            alt_text='中文相似電影推薦',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(yahoo_post(movie_name[0])),
                        title='{}'.format(movie_name[0]),
                        text='中文電影相關推薦:1',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(yahoo_post(movie_name[0]))
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[0])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(yahoo_post(movie_name[1])),
                        title='{}'.format(movie_name[1]),
                        text='中文電影相關推薦:2',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(yahoo_post(movie_name[1]))
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[1])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[1])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(yahoo_post(movie_name[2])),
                        title='{}'.format(movie_name[2]),
                        text='中文電影相關推薦:3',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(yahoo_post(movie_name[2]))
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[2])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[2])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(yahoo_post(movie_name[3])),
                        title='{}'.format(movie_name[3]),
                        text='中文電影相關推薦:4',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(yahoo_post(movie_name[3]))
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[3])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[3])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(yahoo_post(movie_name[4])),
                        title='{}'.format(movie_name[4]),
                        text='中文電影相關推薦:5',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(yahoo_post(movie_name[4]))
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[4])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[4])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(yahoo_post(movie_name[5])),
                        title='{}'.format(movie_name[5]),
                        text='中文電影相關推薦:6',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(yahoo_post(movie_name[5]))
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[5])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[5])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(yahoo_post(movie_name[6])),
                        title='{}'.format(movie_name[6]),
                        text='中文電影相關推薦:7',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(yahoo_post(movie_name[6]))
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[6])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[6])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(yahoo_post(movie_name[7])),
                        title='{}'.format(movie_name[7]),
                        text='中文電影相關推薦:8',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(yahoo_post(movie_name[7]))
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[7])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[7])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(yahoo_post(movie_name[8])),
                        title='{}'.format(movie_name[8]),
                        text='中文電影相關推薦:9',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(yahoo_post(movie_name[8]))
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[8])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[8])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=yahoo_post_path + '{}.jpg'.format(yahoo_post(movie_name[9])),
                        title='{}'.format(movie_name[9]),
                        text='中文電影相關推薦:10',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(yahoo_post(movie_name[9]))
                            ),
                            MessageAction(

                                label='相關推薦',
                                text='中文電影{}的相關推薦'.format(movie_name[9])
                            ),
                            MessageAction(
                                label='網路評價',
                                text='輿論評估：{}'.format(movie_name[9])
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)


    elif ('相關推薦' and '外國') in msg:
        movie_name = mongo_imdb_similarity(msg.split('的相關推薦')[0].split('外國電影')[1])
        message = TemplateSendMessage(
            alt_text='英文相似電影推薦',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[0])),
                        title='{}'.format(movie_name[0]),
                        text='英文電影相關推薦:1',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[0]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[1])),
                        title='{}'.format(movie_name[1]),
                        text='英文電影相關推薦:2',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[1]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[1])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[2])),
                        title='{}'.format(movie_name[2]),
                        text='英文電影相關推薦:3',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[2]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[2])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[3])),
                        title='{}'.format(movie_name[3]),
                        text='英文電影相關推薦:4',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[3]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[3])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[4])),
                        title='{}'.format(movie_name[4]),
                        text='英文電影相關推薦:5',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[4]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[4])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[5])),
                        title='{}'.format(movie_name[5]),
                        text='英文電影相關推薦:6',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[5]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[5])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[6])),
                        title='{}'.format(movie_name[6]),
                        text='英文電影相關推薦:7',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[6]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[6])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[7])),
                        title='{}'.format(movie_name[7]),
                        text='英文電影相關推薦:8',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[7]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[7])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[8])),
                        title='{}'.format(movie_name[8]),
                        text='英文電影相關推薦:9',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[8]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[8])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[9])),
                        title='{}'.format(movie_name[9]),
                        text='英文電影相關推薦:10',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[9]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[9])
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    elif msg == '熱議電影':
        red = redis.StrictRedis(host=GCP_IP, port=6379, db=0)
        hot_imgurl_list=['hotimg_0','hotimg_1','hotimg_2','hotimg_3','hotimg_4','hotimg_5','hotimg_6','hotimg_7','hotimg_8','hotimg_9']
        hot_name_list=['hotname_0','hotname_1','hotname_2','hotname_3','hotname_4','hotname_5','hotname_6','hotname_7','hotname_8','hotname_9']
        hot_url_list=['hoturl_0','hoturl_1','hoturl_2','hoturl_3','hoturl_4','hoturl_5','hoturl_6','hoturl_7','hoturl_8','hoturl_9',]
        hot_imgurl_list=red.mget(hot_imgurl_list)
        hot_name_list=red.mget(hot_name_list)
        hot_url_list=red.mget(hot_url_list)
        message = TemplateSendMessage(
            alt_text='熱議排名前10',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=hot_imgurl_list[0].decode('utf-8'),
                        title='{}'.format(hot_name_list[0].decode('utf-8')),
                        text='熱議排名：1',
                        actions=[
                            URIAction(
                            label='電影介紹',
                            uri=hot_url_list[0].decode('utf-8')
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=hot_imgurl_list[1].decode('utf-8'),
                        title='{}'.format(hot_name_list[1].decode('utf-8')),
                        text='熱議排名：2',
                        actions=[
                            URIAction(
                                label='電影介紹',
                                uri=hot_url_list[1].decode('utf-8')
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=hot_imgurl_list[2].decode('utf-8'),
                        title='{}'.format(hot_name_list[2].decode('utf-8')),
                        text='熱議排名：3',
                        actions=[
                            URIAction(
                                label='電影介紹',
                                uri=hot_url_list[2].decode('utf-8')
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=hot_imgurl_list[3].decode('utf-8'),
                        title='{}'.format(hot_name_list[3].decode('utf-8')),
                        text='熱議排名：4',
                        actions=[
                            URIAction(
                                label='電影介紹',
                                uri=hot_url_list[3].decode('utf-8')
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=hot_imgurl_list[4].decode('utf-8'),
                        title='{}'.format(hot_name_list[4].decode('utf-8')),
                        text='熱議排名：5',
                        actions=[
                            URIAction(
                                label='電影介紹',
                                uri=hot_url_list[4].decode('utf-8')
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=hot_imgurl_list[5].decode('utf-8'),
                        title='{}'.format(hot_name_list[5].decode('utf-8')),
                        text='熱議排名：6',
                        actions=[
                            URIAction(
                                label='電影介紹',
                                uri=hot_url_list[5].decode('utf-8')
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=hot_imgurl_list[6].decode('utf-8'),
                        title='{}'.format(hot_name_list[6].decode('utf-8')),
                        text='熱議排名：7',
                        actions=[
                            URIAction(
                                label='電影介紹',
                                uri=hot_url_list[6].decode('utf-8')
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=hot_imgurl_list[7].decode('utf-8'),
                        title='{}'.format(hot_name_list[7].decode('utf-8')),
                        text='熱議排名：8',
                        actions=[
                            URIAction(
                                label='電影介紹',
                                uri=hot_url_list[7].decode('utf-8')
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=hot_imgurl_list[8].decode('utf-8'),
                        title='{}'.format(hot_name_list[8].decode('utf-8')),
                        text='熱議排名：9',
                        actions=[
                            URIAction(
                                label='電影介紹',
                                uri=hot_url_list[8].decode('utf-8')
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=hot_imgurl_list[9].decode('utf-8'),
                        title='{}'.format(hot_name_list[9].decode('utf-8')),
                        text='熱議排名：10',
                        actions=[
                            URIAction(
                                label='電影介紹',
                                uri=hot_url_list[9].decode('utf-8')
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    elif msg == '喜好推薦':
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
        userId = json.loads(body)['events'][0]['source']['userId']
        movie_name=personal_favor(userId)
        message = TemplateSendMessage(
            alt_text='個人喜好推薦結果',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path+'{}.jpg'.format(mongo_imdb_name_to_id(movie_name[0])),
                        title='{}'.format(movie_name[0]),
                        text='個人喜好推薦:1',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[0]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[0])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[1])),
                        title='{}'.format(movie_name[1]),
                        text='個人喜好推薦:2',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[1]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[1])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[2])),
                        title='{}'.format(movie_name[2]),
                        text='個人喜好推薦:3',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[2]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[2])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[3])),
                        title='{}'.format(movie_name[3]),
                        text='個人喜好推薦:4',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[3]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[3])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[4])),
                        title='{}'.format(movie_name[4]),
                        text='個人喜好推薦:5',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[4]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[4])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[5])),
                        title='{}'.format(movie_name[5]),
                        text='個人喜好推薦:6',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[5]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[5])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[6])),
                        title='{}'.format(movie_name[6]),
                        text='個人喜好推薦:7',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[6]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[6])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[7])),
                        title='{}'.format(movie_name[7]),
                        text='個人喜好推薦:8',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[7]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[7])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[8])),
                        title='{}'.format(movie_name[8]),
                        text='個人喜好推薦:9',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[8]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[8])
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=imdb_post_path + '{}.jpg'.format(mongo_imdb_name_to_id(movie_name[9])),
                        title='{}'.format(movie_name[9]),
                        text='個人喜好推薦:10',
                        actions=[
                            PostbackAction(
                                label='喜歡這部電影',
                                data='喜歡電影的id:{}'.format(mongo_imdb_name_to_id(movie_name[9]))
                            ),
                            MessageAction(
                                label='相關推薦',
                                text='外國電影{}的相關推薦'.format(movie_name[9])
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)


import pymysql,random
def sql_animation(movie_name):
    host = GCP_IP
    port = 3306
    user = 'root'
    passwd = 'example'
    db = 'mysql'
    charset = 'utf8mb4'
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor()
    sql_select = "select primaryTitle,id,group_id from movie_group_id WHERE {} = 1;".format(movie_name)
    cursor.execute(sql_select)
    row_2 = cursor.fetchall()
    m_list=random.sample(row_2, k=3)
    conn.commit()
    cursor.close()
    conn.close()
    print(m_list)
    return m_list

def yahoo_post(movie_name):
    con = MongoClient('mongodb://'+ GCP_IP +':27017/')
    db = con.Movie_project
    dis = db.movie_similarity.find({'電影中文名': "{}".format(movie_name)})
    dis = list(dis)
    yahoo_post_id = dis[0]['_id']
    return yahoo_post_id

def mongo_imdb():
    con = MongoClient('mongodb://'+ GCP_IP +':27017/')
    db = con.Movie_project
    dis = db.movie_similarity_IMDB_new.find()
    dis = list(dis)
    dis = random.sample(dis, k=10)
    return dis

def mongo_imdb_similarity(movie_name):
    con = MongoClient('mongodb://'+ GCP_IP +':27017/')
    db = con.Movie_project
    dis = db.movie_similarity_IMDB_new.find({'IMDB電影名': "{}".format(movie_name)})
    dis = list(dis)
    dis=list(dis[0]['其他電影相似度'].keys())[:10]
    return dis

def mongo_imdb_name_to_id(movie_name):
    con = MongoClient('mongodb://'+ GCP_IP +':27017/')
    db = con.Movie_project
    dis = db.movie_similarity_IMDB_new.find({'IMDB電影名': "{}".format(movie_name)})
    dis = list(dis)
    dis = dis[0]['_id']
    return dis

def personal_favor(userId):
    con = MongoClient('mongodb://'+ GCP_IP +':27017/')
    db = con.yun
    dis = db.personal_favor_log.find({'userId':userId})
    name_list = [imdb_id['imdbId'] for imdb_id in dis]
    name_list = random.sample(name_list, k=3)
    host = GCP_IP
    port = 3306
    user = 'root'
    passwd = 'example'
    db = 'mysql'
    charset = 'utf8mb4'
    a = name_list[0]
    b = name_list[1]
    c = name_list[2]

    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor()
    sql_set = 'SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode, "ONLY_FULL_GROUP_BY,", ""));'
    sql = 'SELECT COUNT(out_id)AS times, sum(sim)/COUNT(out_id) AS avg_sim, sum(con) AS sum_con, out_id, movie_name\n'\
    +'FROM movie_spark\n'\
    +'WHERE in_id="%s" OR in_id="%s" OR in_id="%s"\n' % (a, b, c)\
    +'GROUP BY out_id\n'\
    +'HAVING avg(sim)\n'\
    +'ORDER BY times DESC , sum_con DESC\n'\
    +'LIMIT 10;\n'

    ce_set = cursor.execute(sql_set)
    ce = cursor.execute(sql)
    content = cursor.fetchall()
    favor_name = [(i[4]) for i in content]
    cursor.close()
    conn.close()
    return favor_name


import joblib
import re
import jieba
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
def comment_use(msg):
    clf = joblib.load("model_cut.m")
    bow_transformer = joblib.load("trans_cut.m")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    # a = input('請輸入要查詢的電影') + (' 電影 評論')
    a=msg
    # Google 搜尋 URL
    google_url = 'https://www.google.com/search?q=%s' %(a)
    r = requests.get(google_url, headers = headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    context_list = soup.select('span[class="st"]')
    g = 0
    b = 0
    for i in context_list:
        text = i.text
        print(i.text)
        text_transformed = bow_transformer.transform([text])
        c = clf.predict(text_transformed)[0]
        if c == 1:
            g += 1
        else:
            b += 1
    page = soup.select('a[aria-label="Page 2"]')
    for i in page:
        print(i['href'])
        google_url_page2 = 'https://www.google.com' + i['href']
    r2 = requests.get(google_url_page2, headers = headers)
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    context_list2 = soup2.select('span[class="st"]')
    stopwords = [line.strip() for line in open('./jieba_data/baidu_stopwords.txt',encoding='UTF-8').readlines()]
    for i in context_list2:
        text = i.text
        print(i.text)
        text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]", "", text)
        ltext = jieba.lcut(text)
        res_text = []
        for word in ltext:
            if word not in stopwords:
                res_text.append(word)
        text_transformed = bow_transformer.transform(res_text)
        c = clf.predict(text_transformed)[0]
        if c == 1:
            g += 1
        else:
            b += 1
    print(a,'的好評有',g,'篇')
    print(a,'的負評有',b,'篇')
    return g,b


from confluent_kafka import Producer
import sys
import time

def kaf_producer(body):
    # 用來接收從Consumer instance發出的error訊息
    def error_cb(err):
        print('Error: %s' % err)

    # 步驟1. 設定要連線到Kafka集群的相關設定
    props = {
        # Kafka集群在那裡?
        'bootstrap.servers': GCP_IP + ':9092',  # <-- 置換成要連接的Kafka集群
        'error_cb': error_cb  # 設定接收error訊息的callback函數
    }
    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(props)
    # 步驟3. 指定想要發佈訊息的topic名稱
    topicName = 'linebot_log_topic'
    msgCounter = 0
    try:
        # produce(topic, [value], [key], [partition], [on_delivery], [timestamp], [headers])
        producer.produce(topicName,partition=0, value=body)
        producer.flush()
        print('Send ' + str(msgCounter) + ' messages to Kafka')
    except BufferError as e:
        # 錯誤處理
        sys.stderr.write('%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                         .format(len(producer)))
    except Exception as e:
        print(e)
    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()

def kaf_producer_like(userId,imdbId):
    # 用來接收從Consumer instance發出的error訊息
    def error_cb(err):
        print('Error: %s' % err)

    # 步驟1. 設定要連線到Kafka集群的相關設定
    props = {
        # Kafka集群在那裡?
        'bootstrap.servers': GCP_IP + ':9092',  # <-- 置換成要連接的Kafka集群
        'error_cb': error_cb  # 設定接收error訊息的callback函數
    }
    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(props)
    # 步驟3. 指定想要發佈訊息的topic名稱
    topicName = 'linebot_log_topic'
    msgCounter = 0
    try:
        # produce(topic, [value], [key], [partition], [on_delivery], [timestamp], [headers])
        movie_like={'userId':userId,'imdbId':imdbId}
        producer.produce(topicName,partition=1,value=str(movie_like))
        producer.flush()
        print('Send ' + str(msgCounter) + ' messages to Kafka')
    except BufferError as e:
        # 錯誤處理
        sys.stderr.write('%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                         .format(len(producer)))
    except Exception as e:
        print(e)
    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()

from flask import render_template
from elasticsearch import Elasticsearch
@app.route("/prediction",methods=['GET','POST'])
def prediction():
    if request.method == 'POST':
        group_list=[]
        budget=3.597 *10000
        try:
            budget_view=float(request.values['n_budget'])
            budget=float(request.values['n_budget']) * budget
        except:
            budget=0
            pass
        try:
            fantasy = request.values['n_fantasy']
            fantasy = -59002565.873
            group_list.append('奇幻')
        except:
            fantasy=0
            pass
        try:
            action = request.values['n_action']
            action = -43947852.946
            group_list.append('動作')
        except:
            action=0
            pass
        try:
            horror = request.values['n_horror']
            horror = 42885605.750
            group_list.append('恐怖')
        except:
            horror=0
            pass
        try:
            adventure = request.values['n_adventure']
            adventure = 36300043.894
            group_list.append('冒險')
        except:
            adventure=0
            pass
        try:
            family = request.values['n_family']
            family = -54738677.841
            group_list.append('家庭')
        except:
            family=0
            pass

        total=int((budget + fantasy +action + horror + adventure + family)/10000)
        change_total=int(total/10000)
        len_total=str(total)
        budget_unit=''
        if len(len_total) >= 5:
            change_total=float(total)/10000
            budget_unit='億'
        else:
            change_total=total
            budget_unit='萬'

        es = Elasticsearch('http://'+ GCP_IP +':9200')
        doc = {'user': 'yunshen',
               '電影預算': budget_view,
               '預測票房': total,
               '分類':str(group_list).replace("'","")
               }
        res = es.index(index='prediction', doc_type='elk', body=doc)
        print(res['result'])
        return render_template('predict.html',**locals())
    else:
        return render_template('predict.html')

'''
啟動Server
'''
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
