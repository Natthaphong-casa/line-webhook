from fastapi import FastAPI, Request, HTTPException
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)

import os

app = FastAPI()

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

configuration = Configuration(
    access_token=CHANNEL_ACCESS_TOKEN
)


@app.get("/")
def home():
    return {"status": "Visitor Registration API Running"}


@app.post("/send")
async def send_message(request: Request):

    body = await request.json()

    group_id = body.get("groupId")

    if not group_id:
        raise HTTPException(status_code=400, detail="groupId missing")

    message = f"""
📋 Visitor Registration

📅 Visit Date : {body.get('visit_date')}
🏢 Company : {body.get('company')}
👤 Visitor : {body.get('name')}
📝 Purpose : {body.get('purpose')}
👨 Contact : {body.get('contact_person')}
🏬 Department : {body.get('department')}
🎫 Visitor Card : {body.get('visitor_card')}
👥 People : {body.get('people')}
"""

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        line_bot_api.push_message(
            PushMessageRequest(
                to=group_id,
                messages=[
                    TextMessage(
                        text=message
                    )
                ]
            )
        )

    return {"success": True}
