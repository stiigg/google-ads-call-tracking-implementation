#!/usr/bin/env bash
set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use relative path to Python script (one level up, then into api-integrations)
python3 "${SCRIPT_DIR}/../api-integrations/google-ads-api/upload-conversions.py"
