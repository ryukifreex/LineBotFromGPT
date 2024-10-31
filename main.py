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
            event.reply_token,
            TextSendMessage(text="認証に失敗しました。登録されたユーザーのみ使用できます。"),
            # TextSendMessage(text="Authentication failed. Only registered users can access this feature."),
        )
        return

    # ユーザーからのメッセージを取得
    input_text = event.message.text
    # テキストに付与するメッセージ
    # add_message = "下記問い合わせに対し犬の真似をして可愛く答えてください"
    # add_message = "あなたは、相手の悩みや悲しみに寄り添い、包み込むような優しさを持つイケメンです。相談者が話しやすいよう、温かく共感し、心のこもったアドバイスや励ましの言葉を提供してください。"
    # add_message = "You are a kind, compassionate person who is deeply empathetic toward others' sadness and struggles. Please respond with warmth and understanding, offering heartfelt advice and words of encouragement to help the person feel at ease and supported."
    add_message = ""
    prompt = f"User: {add_message}\n{input_text}\nChatGPT: "

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
