## English

This project is a Line Bot application that uses ChatGPT. It enables users to communicate with ChatGPT directly through the Line messaging app. By assigning a value to the add_message variable, you can add custom instructions to control the bot's responses.
Requirements
To run this application, the following environment variables need to be set up:
LINE_CHANNEL_ACCESS_TOKEN: Access token for the Line Messaging API.
LINE_CHANNEL_SECRET: Secret key for Line Webhook.
OPENAI_API_KEY: API key for OpenAI (ChatGPT).
REGISTERED_USERS: A comma-separated list of user IDs registered to use this bot.

Example:

```python
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])
openai.api_key = os.environ["OPENAI_API_KEY"]
registered_users = os.environ["REGISTERED_USERS"].split(",")
```

### Usage

-   Set the environment variables as specified above.
-   Assign any custom instruction to add_message to adjust the bot’s behavior.
-   Start the bot to communicate with ChatGPT through the Line application.

## 日本語

このプロジェクトは、ChatGPT を利用した Line Bot アプリケーションです。Line のメッセージングアプリを通じて、直接 ChatGPT と対話することができます。add_message 変数に任意の指示内容を設定することで、Bot の応答にカスタム指示を追加できます。
必要な設定
このアプリケーションを動作させるには、以下の環境変数の設定が必要です：

-   LINE_CHANNEL_ACCESS_TOKEN: Line Messaging API のアクセストークン
-   LINE_CHANNEL_SECRET: Line Webhook のシークレットキー
-   OPENAI_API_KEY: OpenAI (ChatGPT) の API キー
-   REGISTERED_USERS: Bot の利用を許可されたユーザー ID のカンマ区切りリスト

例:

```python
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])
openai.api_key = os.environ["OPENAI_API_KEY"]
registered_users = os.environ["REGISTERED_USERS"].split(",")
```

### 使用方法

-   上記の環境変数を設定します。
-   add_message に任意の指示を設定して、Bot の応答を調整します。
-   Bot を起動し、Line アプリを通じて ChatGPT と対話を開始します。
