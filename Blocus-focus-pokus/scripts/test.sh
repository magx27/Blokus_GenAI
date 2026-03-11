#!/usr/bin/env bash
set -euo pipefail

if [ -f .venv/bin/activate ]; then
  . .venv/bin/activate
else
  export PYTHONPATH=src
fi

python -m unittest discover -s tests -v

