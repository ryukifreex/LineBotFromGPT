from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os
from dotenv import load_dotenv

load_dotenv()
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])
openai.api_key = os.environ["OPENAI_API_KEY"]
registered_users = os.environ["REGISTERED_USERS"].split(",")

app = FastAPI()
@app.get("/")
def testPage():
  return {"testss":"hello world"}

# LineWebhookBodyモデル
class LineWebhookBody(BaseModel):
    events: list
    destination: str

# エンドポイント
@app.post("/callback")
async def callback(request: Request):
    # LINEからのリクエスト署名とボディを取得
    line_signature = request.headers["X-Line-Signature"]
    body = await request.body()

    try:
        # LINEのハンドラにリクエストを渡す
        handler.handle(body.decode("utf-8"), line_signature)
    except InvalidSignatureError:
        # 署名が無効な場合、エラーを返す
        raise HTTPException(status_code=400)
    return "OK"

# MessageEvent発生時（メッセージ受信時）
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # ユーザーIDを取得
    user_id = event.source.user_id
    # 認証済みユーザーのみがアクセスできるようにする
    if user_id not in registered_users:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="認証に失敗しました。登録されたユーザーのみ使用できます。")
        )
        return

    # ユーザーからのメッセージを取得
    input_text = event.message.text
    # add_message = "という質問を「考え方」で回答してください"
    add_message=""
    prompt = f"User: {input_text}\n{add_message}\nChatGPT: "

    # botへのリクエストを生成
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        # botの返答を取得してLINEに送信
        reply_text = response.choices[0].text.strip()
        return line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    # エラー時
    except:
        return "申し訳ございません。しばらくしてからもう一度お試しください。"