#!/bin/bash -e

if [ -f .venv/bin/activate ]; then
    echo "Load Python virtualenv from '.venv/bin/activate'"
    source .venv/bin/activate
fi

exec "$@"
