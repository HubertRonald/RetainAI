FROM mcr.microsoft.com/devcontainers/python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV OMP_NUM_THREADS=1
ENV PATH="/root/.pulumi/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    git \
    graphviz \
    build-essential \
    curl \
    libgomp1 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://get.pulumi.com | sh

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" \
    -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf aws awscliv2.zip

WORKDIR /workspace

COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY modules ./modules
COPY requirements ./requirements

RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install -e ".[dev,test]"

CMD ["bash"]