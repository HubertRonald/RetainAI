from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from apps.api.routers import explainability, overview, prediction, survival


app = FastAPI(
    title="RetainAI API",
    description="API service for RetainAI dashboard and employee retention intelligence.",
    version="0.1.0",
)


@app.get("/", response_class=HTMLResponse)
def index(_: Request) -> Any:
    """Styled root page aligned with the RetainAI dashboard theme."""

    html_body = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>RetainAI API</title>
        <style>
          :root {
            --bg: #1d293d;
            --panel: #0f172b;
            --panel-2: #111c33;
            --text: #e2e8f0;
            --muted: #94a3b8;
            --primary: #615fff;
            --purple: #8b5cf6;
            --pink: #ec4899;
            --green: #22c55e;
            --border: #314158;
          }

          * {
            box-sizing: border-box;
          }

          body {
            margin: 0;
            min-height: 100vh;
            padding: 48px 24px;
            background:
              radial-gradient(circle at 20% 0%, rgba(97, 95, 255, 0.20), transparent 34%),
              radial-gradient(circle at 80% 12%, rgba(236, 72, 153, 0.12), transparent 30%),
              linear-gradient(135deg, #0b1120 0%, var(--bg) 45%, #111827 100%);
            color: var(--text);
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          }

          .card {
            max-width: 820px;
            margin: auto;
            padding: 34px;
            background: linear-gradient(180deg, rgba(17, 28, 51, 0.94), rgba(15, 23, 43, 0.96));
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 20px;
            box-shadow: 0 24px 70px rgba(2, 8, 23, 0.55);
          }

          .brand {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 20px;
          }

          .logo {
            width: 54px;
            height: 54px;
            display: grid;
            place-items: center;
            border-radius: 16px;
            background: rgba(97, 95, 255, 0.16);
            border: 1px solid rgba(139, 92, 246, 0.38);
            box-shadow: 0 0 30px rgba(97, 95, 255, 0.18);
          }

          .brand h1 {
            margin: 0;
            font-size: 2.35rem;
            letter-spacing: -0.045em;
            line-height: 1;
            font-weight: 800;
          }

          .brand .ai {
            color: var(--purple);
            text-shadow: 0 0 18px rgba(139, 92, 246, 0.35);
          }

          .subtitle {
            margin: 0;
            color: var(--muted);
            font-size: 1rem;
          }

          .hero {
            margin-top: 26px;
            padding: 24px;
            border-radius: 16px;
            background: rgba(15, 23, 42, 0.62);
            border: 1px solid rgba(148, 163, 184, 0.16);
          }

          .hero h2 {
            margin: 0 0 10px 0;
            font-size: 1.45rem;
            letter-spacing: -0.025em;
          }

          .hero p {
            margin: 0;
            color: #cbd5e1;
            line-height: 1.6;
          }

          .chips {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 24px;
          }

          .chip {
            padding: 8px 12px;
            border-radius: 999px;
            border: 1px solid rgba(148, 163, 184, 0.20);
            background: rgba(15, 23, 42, 0.72);
            color: #cbd5e1;
            font-size: 0.86rem;
          }

          .chip.green {
            color: #86efac;
            border-color: rgba(34, 197, 94, 0.28);
            background: rgba(34, 197, 94, 0.08);
          }

          .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 28px;
          }

          .button {
            display: inline-block;
            padding: 12px 18px;
            border-radius: 12px;
            color: white;
            text-decoration: none;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--purple));
            border: 1px solid rgba(139, 92, 246, 0.42);
          }

          .button.secondary {
            background: rgba(30, 41, 59, 0.86);
            border-color: rgba(148, 163, 184, 0.28);
          }

          .footer {
            margin-top: 28px;
            padding-top: 18px;
            border-top: 1px solid rgba(148, 163, 184, 0.16);
            color: var(--muted);
            font-size: 0.88rem;
            text-align: center;
          }

          .footer a {
            color: #a78bfa;
            text-decoration: none;
            font-weight: 700;
          }
        </style>
      </head>

      <body>
        <main class="card">
          <section class="brand">
            <div class="logo">
              <svg width="34" height="34" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M24 11c-5.2 0-9.4 4.2-9.4 9.4 0 .6.1 1.2.2 1.8A10.3 10.3 0 0 0 9 31.6c0 3.9 2.2 7.3 5.4 9A10.4 10.4 0 0 0 24.8 53H29V11h-5Z" stroke="#8b5cf6" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M40 11c5.2 0 9.4 4.2 9.4 9.4 0 .6-.1 1.2-.2 1.8A10.3 10.3 0 0 1 55 31.6c0 3.9-2.2 7.3-5.4 9A10.4 10.4 0 0 1 39.2 53H35V11h5Z" stroke="#2f7df6" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M22 22c3.6 0 5.8 2.1 7 5M20 35c3.7-.5 6.6.7 9 3.6M42 22c-3.6 0-5.8 2.1-7 5M44 35c-3.7-.5-6.6.7-9 3.6" stroke="#ec4899" stroke-width="3" stroke-linecap="round"/>
                <circle cx="32" cy="32" r="4.5" fill="#22c55e"/>
              </svg>
            </div>
            <div>
              <h1>Retain<span class="ai">AI</span> API</h1>
              <p class="subtitle">Employee Retention Intelligence Service</p>
            </div>
          </section>

          <section class="hero">
            <h2>Welcome to the RetainAI API</h2>
            <p>
              This service powers the RetainAI dashboard with prediction,
              explainability, survival analytics and overview endpoints.
              It is designed to support local, containerized and future AWS-ready execution.
            </p>
          </section>

          <section class="chips">
            <span class="chip green">Status: online</span>
            <span class="chip">Runtime: container/local</span>
            <span class="chip">Port: 8001</span>
            <span class="chip">Version: 0.1.0</span>
          </section>

          <section class="actions">
            <a class="button" href="/docs">Open API Docs</a>
            <a class="button secondary" href="/health">Health Check</a>
            <a class="button secondary" href="/openapi.json">OpenAPI JSON</a>
          </section>

          <section class="footer">
            Coded with ♥ by
            <a href="https://hubertronald.github.io/" target="_blank">Hubert Ronald</a>
          </section>
        </main>
      </body>
    </html>
    """

    return HTMLResponse(content=html_body)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "retainai-api"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(overview.router)
app.include_router(prediction.router)
app.include_router(explainability.router)
app.include_router(survival.router)
