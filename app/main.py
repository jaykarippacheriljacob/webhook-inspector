"""
Application entry point.

This file stays tiny on purpose: it creates the FastAPI app, mounts the two
route groups, and serves the dashboard at /. Run it with:

    uvicorn app.main:app --reload
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.dashboard import DASHBOARD_HTML
from app.routers import inspect, webhook

app = FastAPI(title="Webhook Inspector", version="1.0.0")

app.include_router(webhook.router)
app.include_router(inspect.router)


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return DASHBOARD_HTML