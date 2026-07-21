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

    print("========== SEND ==========")
    print(data)
    print("==========================")

    return {
        "success": True
    }
