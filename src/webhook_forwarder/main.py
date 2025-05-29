from fastapi import FastAPI, Request, HTTPException
from webhook_forwarder.config import (
    OAUTH_TOKEN_URL, CLIENT_ID, CLIENT_SECRET,
    USERNAME, PASSWORD, FORWARD_URL
)
import httpx

app = FastAPI()

async def get_bearer_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            OAUTH_TOKEN_URL,
            data={
                "grant_type": "password",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "username": USERNAME,
                "password": PASSWORD,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to retrieve token")
        return response.json().get("access_token")

@app.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    token = await get_bearer_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        forward_response = await client.post(FORWARD_URL, json=payload, headers=headers)

    return {
        "status": "forwarded",
        "forward_status": forward_response.status_code
    }
