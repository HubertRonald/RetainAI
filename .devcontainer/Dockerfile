FROM mcr.microsoft.com/devcontainers/python:3.10

ARG TARGETARCH
ARG PULUMI_VERSION=3.142.0

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV OMP_NUM_THREADS=1

# Base OS tooling for RetainAI + cloud CLIs.
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    ca-certificates \
    curl \
    direnv \
    git \
    gnupg \
    graphviz \
    jq \
    less \
    libgomp1 \
    lsb-release \
    make \
    openssh-client \
    unzip \
    wget \
    zip \
    && rm -rf /var/lib/apt/lists/*

# AWS CLI v2.
RUN set -eux; \
    case "${TARGETARCH}" in \
      "arm64") AWS_ARCH="aarch64" ;; \
      *) AWS_ARCH="x86_64" ;; \
    esac; \
    curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-${AWS_ARCH}.zip" -o "awscliv2.zip"; \
    unzip -q awscliv2.zip; \
    ./aws/install; \
    rm -rf aws awscliv2.zip

# Google Cloud CLI.
RUN set -eux; \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
      | gpg --batch --yes --dearmor -o /usr/share/keyrings/cloud.google.gpg; \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
      > /etc/apt/sources.list.d/google-cloud-sdk.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      google-cloud-cli \
      google-cloud-cli-gke-gcloud-auth-plugin \
      google-cloud-cli-cloud-build-local \
      google-cloud-cli-cloud-run-proxy \
      google-cloud-cli-tests \
      ffmpeg libsm6 libxext6 \
      direnv; \
    rm -rf /var/lib/apt/lists/*

# GitHub CLI fallback install for Debian-based DevContainer.
RUN set -eux; \
    mkdir -p -m 755 /etc/apt/keyrings; \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
      | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg >/dev/null; \
    chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
      > /etc/apt/sources.list.d/github-cli.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends gh; \
    rm -rf /var/lib/apt/lists/*

# Docker CLI only. Docker daemon stays on the host through docker-outside-of-docker.
RUN set -eux; \
    mkdir -p -m 0755 /etc/apt/keyrings; \
    curl -fsSL https://download.docker.com/linux/debian/gpg \
      | gpg --batch --yes --dearmor -o /etc/apt/keyrings/docker.gpg; \
    chmod a+r /etc/apt/keyrings/docker.gpg; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
      > /etc/apt/sources.list.d/docker.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      docker-ce-cli \
      docker-buildx-plugin \
      docker-compose-plugin; \
    rm -rf /var/lib/apt/lists/*

# Pulumi CLI.
RUN set -eux; \
    curl -fsSL https://get.pulumi.com | sh -s -- --version "${PULUMI_VERSION}"; \
    install -m 0755 /root/.pulumi/bin/pulumi /usr/local/bin/pulumi; \
    rm -rf /root/.pulumi

# Shell helpers.
RUN echo 'eval "$(direnv hook bash)"' >> /home/vscode/.bashrc \
    && echo 'if [ -f /workspace/.venv/bin/activate ]; then echo "Run: . ./.venv/bin/activate"; fi' >> /home/vscode/.bashrc \
    && chown -R vscode:vscode /home/vscode

WORKDIR /workspace

CMD ["bash"]
