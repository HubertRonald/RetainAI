FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV RETAINAI_DASHBOARD_MODE=api
ENV RETAINAI_API_URL=http://api:8001

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY modules ./modules
COPY apps/dashboard ./apps/dashboard
COPY artifacts ./artifacts
COPY data ./data

RUN python -m pip install --upgrade pip setuptools wheel && python -m pip install -e ".[dashboard]"

EXPOSE 8501

CMD ["streamlit", "run", "apps/dashboard/streamlit-app/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
