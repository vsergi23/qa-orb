#!/usr/bin/env sh
xvfb-run -a --server-args="-screen 0 1366x768x24" python3 -m pytest -v "$@"
