import whisper
import tempfile
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, AudioMessage

app = Flask(__name__)
line_bot_api = LineBotApi("Channel access token")
handler = WebhookHandler("Channel secret")

model = whisper.load_model("small")

@app.route("/", methods=["POST"])
def root():
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

@handler.add(MessageEvent, message=AudioMessage)
def audio_message(event):
   content = line_bot_api.get_message_content(event.message.id)
   audio_content = content
   with tempfile.NamedTemporaryFile(suffix=".mp3") as tf:
       for chuck in audio_content.iter_content():
           tf.write(chuck)
       result = model.transcribe(tf.name, initial_prompt="今天的天氣、空氣都很好，適合出外郊遊。從陽台望出去，翠綠的平原盡收眼底，都市彷彿遠在天邊。什麼時候要出門呢？")
       line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result["text"]))


if __name__ == "__main__":
    app.run()

