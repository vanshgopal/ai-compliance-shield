import os
import secrets
from urllib.parse import urlencode

import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

app = FastAPI(title="AI Compliance Shield - Google Ads Read-only Bridge")

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
ADS_API_BASE = "https://googleads.googleapis.com/v26"

def setting(name: str, required: bool = True):
    value = os.getenv(name, "").strip()
    if required and not value:
        raise HTTPException(status_code=503, detail=f"Missing Render environment variable: {name}")
    return value

def serializer():
    return URLSafeTimedSerializer(setting("APP_SECRET"))

def page(message: str, status: int = 200):
    return HTMLResponse(
        "<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Google Ads connection</title></head><body style='font:16px Arial;max-width:760px;margin:40px auto;padding:0 18px'>"
        + message + "</body></html>",
        status_code=status,
    )

@app.get("/", response_class=HTMLResponse)
def home():
    return page(
        "<h2>AI Compliance Shield – Google Ads connection</h2>"
        "<p>This separate service is designed for read-only reporting. It does not create, edit, or pause campaigns.</p>"
        "<p><a href='/connect'>Connect Google Ads account</a></p>"
        "<p>After connection, the service owner must save the refresh token in Render environment variables.</p>"
    )

@app.get("/connect")
def connect():
    client_id = setting("GOOGLE_ADS_CLIENT_ID")
    redirect_uri = setting("GOOGLE_ADS_REDIRECT_URI")
    state = secrets.token_urlsafe(32)
    signed_state = serializer().dumps(state)
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/adwords",
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
        "state": state,
    }
    response = RedirectResponse(GOOGLE_AUTH_URL + "?" + urlencode(params))
    response.set_cookie(
        "ads_oauth_state", signed_state, max_age=600, httponly=True,
        secure=True, samesite="lax"
    )
    return response

@app.get("/oauth/callback", response_class=HTMLResponse)
def oauth_callback(request: Request, code: str = "", state: str = "", error: str = ""):
    if error:
        return page("<h2>Google authorization was not completed</h2><p>" + error + "</p>", 400)
    signed_state = request.cookies.get("ads_oauth_state")
    if not signed_state:
        raise HTTPException(status_code=400, detail="OAuth state cookie is missing. Start again from /connect.")
    try:
        expected_state = serializer().loads(signed_state, max_age=600)
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=400, detail="OAuth state expired or invalid. Start again from /connect.")
    if not state or not secrets.compare_digest(state, expected_state):
        raise HTTPException(status_code=400, detail="OAuth state did not match.")
    if not code:
        raise HTTPException(status_code=400, detail="Google did not return an authorization code.")

    token_response = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "code": code,
            "client_id": setting("GOOGLE_ADS_CLIENT_ID"),
            "client_secret": setting("GOOGLE_ADS_CLIENT_SECRET"),
            "redirect_uri": setting("GOOGLE_ADS_REDIRECT_URI"),
            "grant_type": "authorization_code",
        },
        timeout=30,
    )
    if not token_response.ok:
        raise HTTPException(status_code=400, detail="Google token exchange failed: " + token_response.text[:800])
    token_data = token_response.json()
    refresh_token = token_data.get("refresh_token")
    if not refresh_token:
        return page(
            "<h2>Google account authorized, but no refresh token was returned</h2>"
            "<p>In Google Account permissions, remove this app's access and try Connect again. "
            "Keep the refresh token private.</p>"
        )
    safe_token = refresh_token.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    response = page(
        "<h2>Google Ads authorization successful</h2>"
        "<p><b>Important:</b> This refresh token is a secret. Do not send it in chat or share it with anyone.</p>"
        "<p>Copy it directly into the Render service's Environment page as "
        "<code>GOOGLE_ADS_REFRESH_TOKEN</code>, then save and redeploy.</p>"
        "<textarea readonly style='width:100%;height:100px' onclick='this.select()'>" + safe_token + "</textarea>"
        "<p>After saving it in Render, you can close this page.</p>"
    )
    response.delete_cookie("ads_oauth_state")
    return response

def get_access_token():
    response = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "client_id": setting("GOOGLE_ADS_CLIENT_ID"),
            "client_secret": setting("GOOGLE_ADS_CLIENT_SECRET"),
            "refresh_token": setting("GOOGLE_ADS_REFRESH_TOKEN"),
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    if not response.ok:
        raise HTTPException(status_code=502, detail="Could not refresh Google access token: " + response.text[:800])
    return response.json()["access_token"]

@app.get("/status")
def status():
    return {
        "service": "Google Ads read-only bridge",
        "refresh_token_configured": bool(os.getenv("GOOGLE_ADS_REFRESH_TOKEN", "").strip()),
        "customer_id_configured": bool(os.getenv("GOOGLE_ADS_CUSTOMER_ID", "").strip()),
    }

@app.get("/metrics")
def metrics():
    customer_id = setting("GOOGLE_ADS_CUSTOMER_ID").replace("-", "")
    query = (
        "SELECT customer.id, customer.descriptive_name, "
        "metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions "
        "FROM customer WHERE segments.date DURING LAST_30_DAYS"
    )
    response = requests.post(
        f"{ADS_API_BASE}/customers/{customer_id}/googleAds:search",
        headers={
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        },
        json={"query": query},
        timeout=45,
    )
    if not response.ok:
        raise HTTPException(status_code=502, detail="Google Ads API request failed: " + response.text[:1200])
    rows = response.json().get("results", [])
    return {"period": "LAST_30_DAYS", "customer_id": customer_id, "results": rows}
