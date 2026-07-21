from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)

app = FastAPI(
    title="Visitor Registration API",
    version="2.0.0"
)


@app.get("/")
async def home():
    return {
        "status": "Visitor Registration API Running",
        "version": "2.0.0"
    }
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not LINE_CHANNEL_ACCESS_TOKEN:
    raise Exception("LINE_CHANNEL_ACCESS_TOKEN is not set")
    
configuration = Configuration(
    access_token=LINE_CHANNEL_ACCESS_TOKEN
)

GROUP_ID = "Cc52d4603130c72260883301a5f112fc4"

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


@app.post("/webhook")
async def webhook(request: Request):

    body = await request.body()

    print("========== LINE EVENT ==========")
    print(body.decode("utf-8"))
    print("================================")

    return JSONResponse(
        {
            "status": "ok"
        }
    )

@app.post("/send")
async def send(request: Request):
    try:
        data = await request.json()

        message = data.get("message", "Hello")

        print("========== SEND ==========")
        print("Group ID:", GROUP_ID)
        print("Message:", message)

        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)

            api.push_message(
                PushMessageRequest(
                    to=GROUP_ID,
                    messages=[
                        TextMessage(text=message)
                    ]
                )
            )

        print("LINE Push Success")

        return {
            "success": True
        }

    except Exception as e:
        print("SEND ERROR:", repr(e))
        raise
