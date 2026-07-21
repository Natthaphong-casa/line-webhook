from fastapi import FastAPI, Request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import JoinEvent

import os

app = FastAPI()

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

GROUP_ID = None


@app.get("/")
def home():
    return {"status": "Visitor Registration API Running"}


@app.post("/webhook")
async def webhook(request: Request):

    body = await request.body()

    print(body.decode("utf-8"))

    signature = request.headers.get("X-Line-Signature")

    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        return {"status": "invalid signature"}

    return {"status": "ok"}


@handler.add(JoinEvent)
def handle_join(event):

    global GROUP_ID

    if event.source.type == "group":
        GROUP_ID = event.source.group_id

        with ApiClient(configuration) as api_client:
            MessagingApi(api_client).reply_message(
                {
                    "replyToken": event.reply_token,
                    "messages": [
                        {
                            "type": "text",
                            "text": "✅ Bot joined successfully"
                        }
                    ]
                }
            )


@app.post("/send")
async def send(request: Request):

    global GROUP_ID

    if GROUP_ID is None:
        return {"error": "Group ID not found"}

    body = await request.json()

    text = f"""
📋 Visitor Registration

📅 Date : {body['visit_date']}
🏢 Company : {body['company']}
👤 Name : {body['name']}
📝 Purpose : {body['purpose']}
👨 Contact : {body['contact_person']}
🏬 Department : {body['department']}
👥 People : {body['people']}
"""

    with ApiClient(configuration) as api_client:

        MessagingApi(api_client).push_message(
            PushMessageRequest(
                to=GROUP_ID,
                messages=[TextMessage(text=text)]
            )
        )

    return {"success": True}
