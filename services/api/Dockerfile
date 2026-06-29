FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY modules ./modules
COPY services/api ./services/api

RUN python -m pip install --upgrade pip setuptools wheel && python -m pip install -e ".[api]"

EXPOSE 8001

CMD ["uvicorn", "services.api.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
