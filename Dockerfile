FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SQLALCHEMY_SILENCE_UBER_WARNING=1

# Install dependencies (MySQL, uWSGI, Pillow etc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git gcc g++ make pkg-config \
    default-libmysqlclient-dev \
    libssl-dev zlib1g-dev libjpeg62-turbo-dev \
    nodejs npm \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel setuptools \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir uwsgi

# Copy source code and install
COPY . .
RUN pip install --no-cache-dir .

# Compile JSX (React) static files (required for production)
RUN ./jsx --output-directory bemani/frontend/static/jsx

# Runtime directories
RUN mkdir -p /cache /logs

EXPOSE 5730 8573 18573

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]