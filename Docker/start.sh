#!/usr/bin/env bash

# waiting for Redis
./waitfor.py redis

if [[ -z "$HOSTNAME" ]]; then HOSTNAME="$(hostname)"; fi

celery worker -l INFO --app=client \
              -Q "tests@$HOSTNAME" \
              -n "$HOSTNAME" \
              --without-gossip \
              --heartbeat-interval 30 \
              --max-memory-per-child=120000
