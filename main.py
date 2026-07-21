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

    data = await request.json()

    message = data.get("message", "Hello from Visitor Registration")

    with ApiClient(configuration) as api_client:

        line_bot_api = MessagingApi(api_client)

        line_bot_api.push_message(
            PushMessageRequest(
                to=GROUP_ID,
                messages=[
                    TextMessage(
                        text=message
                    )
                ]
            )
        )

    return {
        "success": True
    }
