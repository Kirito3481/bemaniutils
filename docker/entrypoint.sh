#!/bin/sh
set -eu

MODE="${1:-frontend}"

# uWSGI common options (production)
UWSGI_OPTS="
  --master
  --die-on-term
  --need-app
  --vacuum
  --enable-threads
  --thunder-lock
  --http-keepalive
  --lazy-apps
  --harakiri 120
  --max-requests 5000
  --buffer-size 32768
"

PROCESSES="${UWSGI_PROCESSES:-4}"
THREADS="${UWSGI_THREADS:-2}"

case "$MODE" in
  services)
    PORT="${PORT:-5730}"
    exec uwsgi $UWSGI_OPTS \
      --http-socket 0.0.0.0:${PORT} \
      --processes ${PROCESSES} --threads ${THREADS} \
      --wsgi-file bemani/wsgi/services.wsgi
    ;;

  frontend)
    PORT="${PORT:-8573}"
    # Serve static files directly with uWSGI
    exec uwsgi $UWSGI_OPTS \
      --http-socket 0.0.0.0:${PORT} \
      --processes ${PROCESSES} --threads ${THREADS} \
      --static-map /static=/app/bemani/frontend/static \
      --static-map /jsx=/app/bemani/frontend/static/jsx \
      --wsgi-file bemani/wsgi/frontend.wsgi
    ;;

  api)
    PORT="${PORT:-18573}"
    exec uwsgi $UWSGI_OPTS \
      --http-socket 0.0.0.0:${PORT} \
      --processes ${PROCESSES} --threads ${THREADS} \
      --wsgi-file bemani/wsgi/api.wsgi
    ;;

  scheduler)
    # Run every 5 minutes
    while true; do
      echo "[$(date)] Running scheduler..."
      ./scheduler --config /app/config/server.yaml || true
      sleep 300
    done
    ;;

  *)
    echo "Unknown mode: $MODE (use: services|frontend|api|scheduler)" >&2
    exit 2
    ;;
esac