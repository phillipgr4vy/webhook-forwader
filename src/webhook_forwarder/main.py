from fastapi import FastAPI, Request, HTTPException
from webhook_forwarder.config import (
    OAUTH_TOKEN_URL, CLIENT_ID, CLIENT_SECRET,
    USERNAME, PASSWORD, FORWARD_URL
)
import logging
import httpx

# Configure basic logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
            logger.error(f"Failed to retrieve OAuth token. Status: {response.status_code}, Response: {response.text}")
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

    # Log important fields/attributes of the forward_response
    logger.info(f"Webhook forwarding attempt completed. URL: {FORWARD_URL}, Status: {forward_response.status_code}, Headers: {dict(forward_response.headers)}, Body: {forward_response.text}")
    return {
        "status": "forwarded",
        "forward_status": forward_response.status_code
    }
