# =========================
# 1-STAGE: builder
# =========================
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# =========================
# 2-STAGE: production
# =========================
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# VENV NI KO‘CHIRAMIZ
COPY --from=builder /venv /venv

# MUHIM: PATH GA QO‘SHAMIZ
ENV PATH="/venv/bin:$PATH"

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["bash", "/app/entrypoint.sh"]
