# Push 2 Pad Sensitivity Fix for Ableton Live 12

This script fixes an issue with the Ableton Push 2 where pads require more pressure to trigger clips in **session mode** and **sequencer mode** compared to note mode.

## What it does

It runs in the background and listens for mode changes on the Push 2. Every time Ableton resets the pad sensitivity, the script immediately reapplies the more responsive setting.

## Requirements

- Ableton Live 12
- Python 3.12 — download at [python.org](https://www.python.org/downloads/release/python-3120/) (check **"Add Python to PATH"** during installation)
- Install the required library by running this command once in your terminal:

```
py -3.12 -m pip install mido
```

## How to use

1. Download `push2_sensitivity.py` and `Start_Push2_Sensitivity.bat` and place them in the same folder
2. Open Ableton Live
3. Double-click `Start_Push2_Sensitivity.bat` — a small window will appear in the background
4. That's it! Keep the window open while using Ableton

## Note

The script is set up for a specific MIDI port configuration (output index 1, input index 0). If it doesn't work for you, you may need to adjust the `OUT_PORT_INDEX` and `IN_PORT_INDEX` values at the top of `push2_sensitivity.py`.

To find the correct index for your setup, run this in your terminal:

```python
import mido
print(mido.get_output_names())
print(mido.get_input_names())
```

---

*Created with the help of AI ([Claude](https://claude.ai) by Anthropic).*

---

## macOS version (`push2_pad_fix.py`)

A reworked version for macOS (also works on Windows/Linux) that finds the Push 2 MIDI ports by name instead of by index, applies the setting to all pads, and also re-applies it on a timer.

    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
    ./venv/bin/python push2_pad_fix.py            # keep pads on "regular"
    ./venv/bin/python push2_pad_fix.py --list     # show MIDI ports

**Limits:** only documented sysex is used. The Push 2 interface doc has no command for the note-on threshold itself. "Select Pad Settings" (0x28) has three presets, and "regular" is already the most sensitive. If pads are still stiff on "regular" in every mode, this can't fix it.

## Experimental: lowering the trigger threshold

Findings from reading Live 12's own Push 2 script (`MIDI Remote Scripts/Push2/pad_velocity_curve.py`, `sysex.py`):

- Sensitivity, Gain and Dynamics only shape the velocity curve and the aftertouch range. They don't change what triggers a pad.
- Live sends "Set Pad Parameters" (0x1B) with `t0=33`, `t1=31`, hardcoded for every setting. The interface doc marks both "unused". They look like a press/release threshold pair, but that is **unverified**.

`--t0`/`--t1` override them. Live re-sends its own values when you change Sensitivity/Gain/Dynamics or reconnect, so keep the script running.

    ./venv/bin/python push2_pad_fix.py --t0 20 --monitor    # lighter? (t1 defaults to t0-2)
    ./venv/bin/python push2_pad_fix.py --reset              # back to Live's 33/31

If pads stick, run `--reset` or power-cycle the Push. `--cpmin`/`--cpmax` default to Live's values for its middle Sensitivity index (1220/1570) and are resent with `--t0`.
