#!/usr/bin/env bash


CELERY_DIR="tmp/celery"

celery multi stop tests --pidfile="$CELERY_DIR/pid/%n.pid"
