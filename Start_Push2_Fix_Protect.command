#!/bin/bash
# Double-click to start in "protect" mode: Session and sequencer/loop pads stay a bit
# stiffer than playing pads, but less stiff than Live's default.
exec "$(dirname "$0")/Start_Push2_Fix.command" --protect
