#!/bin/bash
# docker healthcheck UH
url_test=http://localhost:5001/usershub/login
if [ ! -f /tmp/container_healthy ]; then
    curl -f "${url_test}" || exit 1
    touch /tmp/container_healthy
fi