#!/bin/bash
# Double-click to start. Sets itself up the first time, then keeps Push 2 pads on "regular".
cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed. Get it from https://www.python.org/downloads/ and try again."
  read -n 1 -s -r -p "Press any key to close."
  exit 1
fi

if [ ! -d venv ]; then
  echo "First-time setup (takes a minute)..."
  python3 -m venv venv && ./venv/bin/pip install -q -r requirements.txt || {
    echo "Setup failed."; read -n 1 -s -r -p "Press any key to close."; exit 1; }
fi

echo "Leave this window open while you use Ableton. Press Ctrl+C or close the window to stop."
./venv/bin/python -I push2_pad_fix.py "$@"
read -n 1 -s -r -p "Stopped. Press any key to close."
