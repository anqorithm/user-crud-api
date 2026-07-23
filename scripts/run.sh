#!/bin/bash
set -e

uv sync
uv run fastapi dev app/main.py