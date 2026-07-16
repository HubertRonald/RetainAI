FROM public.ecr.aws/lambda/python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH="${LAMBDA_TASK_ROOT}:${LAMBDA_TASK_ROOT}/src"

WORKDIR ${LAMBDA_TASK_ROOT}

# Copiar primero requirements para aprovechar la caché de Docker.
COPY requirements/api-lambda.txt ./requirements/api-lambda.txt

RUN python -m pip install \
    --upgrade \
    pip && \
    python -m pip install \
    --no-cache-dir \
    --requirement requirements/api-lambda.txt

# Código de la aplicación.
COPY apps ./apps
COPY modules ./modules
COPY src ./src
COPY configs ./configs

CMD ["apps.api.lambda_handler.handler"]