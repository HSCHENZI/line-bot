# SDK : software development kit
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

line_bot_api = LineBotApi('1o4+ymRVq4ILZItYEvvGyneFG2p6N38p4qvAZR1PXlf2hDjyL0M9GlSTVFFJEPLaYTH1M8004Br8l8jHP1tI7C8pMQB13BE7LP6Wbc0SVKYhs7bb/nCXUtpfAdDXzZzlf8SMdbdaUR4w6ypjTE9YhwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0f5465110bd7c63afaa6d22df18746e4')

# line接收訊息傳給我們的程式碼接收
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# main通常為主要function 不寫以下這行code ,主要function被import就會直接被執行
if __name__ == "__main__":
    app.run()
