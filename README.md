# Push 2 Pad Fix (macOS)

Keeps the pads on your Ableton Push 2 on their most sensitive setting, in every mode.

**This version is for Mac.** Windows users should use the original project this was forked from: https://github.com/BenDS1984/push2-pad-sensitivity

## The problem

Ableton Live can switch the Push 2 back to a stiffer pad setting when you change modes (for example into Session or Sequencer mode), so pads need more pressure than in Note mode. This app runs in the background and puts the setting back every time.

## What you need

- A Mac with Ableton Live 12 and a Push 2 connected by USB
- Python 3, a free download from https://www.python.org/downloads/ (if you're not sure you have it, the launcher below will tell you)

## Install

1. Go to the [Releases page](../../releases/latest) and download the **Source code (zip)** (or click the green **Code** button on the main page, then **Download ZIP**).
2. Open the downloaded ZIP to unpack it, and move the folder somewhere permanent, like Documents.

## Use

1. Open Ableton Live with your Push 2 connected.
2. In the folder, double-click **Start_Push2_Fix.command**.
   - The first time, macOS will block it because it's a downloaded file. Click **Done** (don't move it to the Trash), then open **System Settings** (**System Preferences** on older macOS) → **Privacy & Security**, scroll to the bottom, and click **Open Anyway** next to the message about `Start_Push2_Fix.command`. Enter your password if asked, then click **Open**. You only need to do this once.
   - On some older versions of macOS, right-clicking the file and choosing **Open** works instead.
   - The first run sets itself up, which takes about a minute.
3. A Terminal window opens and prints that it applied the "regular" setting. **Leave it open** while you use Ableton. Close the window to stop it.

## Troubleshooting

- **"No output port matching 'Push 2 User Port'"**: the Push 2 isn't connected or isn't powered on.
- **Pads still feel stiff in every mode**: this app can only hold the "regular" setting, the most sensitive of the three that Push 2 offers. See the experimental section under Technical / diagnostics below.

---

## Technical / diagnostics

*For people comfortable in Terminal. Run these from the project folder.*

    ./venv/bin/python push2_pad_fix.py [options]

Press **Ctrl+C** to stop. Stopping doesn't undo anything on the Push; the last setting stays until Live changes it or the Push is reconnected.

### Common commands

| Command | What it does |
|---|---|
| `./venv/bin/python push2_pad_fix.py` | Normal use: hold all pads on "regular" |
| `./venv/bin/python push2_pad_fix.py --monitor` | Live readout in Terminal of every pad hit, e.g. `pad 36 (row 1 from bottom, col 1) velocity 18` (velocity 1-127). Handy for seeing how light a touch registers. Touching an encoder or the touch strip also sends a note, shown as `NOT A PAD`. Very low velocities (1-5) can be inaudible, so a pad may show up here without making sound |
| `./venv/bin/python push2_pad_fix.py --list` | List the MIDI ports the Mac can see, then exit. Use it if the Push isn't found |
| `./venv/bin/python push2_pad_fix.py --reset` | Send Live's own threshold values (33/31) once, then exit. Undoes `--t0` |

### All options

| Option | Default | Meaning |
|---|---|---|
| `--setting 0\|1\|2` | `0` | Pad preset: 0 regular (most sensitive), 1 reduced, 2 low |
| `--monitor` | off | Print each pad note-on (pad number, position and velocity); other touches are labeled `NOT A PAD` |
| `--list` | | Show MIDI ports and exit |
| `--reset` | | Send Live's threshold values once and exit |
| `--t0 N` | off | **Experimental.** Override pad parameter 0 (Live sends 33) |
| `--t1 N` | `t0 - 2` | **Experimental.** Override pad parameter 1 (Live sends 31). Must be ≤ `t0` |
| `--cpmin N` | `1220` | Aftertouch lower threshold, sent along with `--t0` (must be > 400) |
| `--cpmax N` | `1570` | Aftertouch upper threshold, sent along with `--t0` (must be > `cpmin`) |
| `--interval S` | `5` | Seconds between background re-applies. `0` turns this off (it then only re-applies on mode changes) |
| `--out NAME` | `Push 2 User Port` | Part of the MIDI output port name to send to |
| `--in NAME` | `Push 2 Live Port` | Part of the MIDI input port name to listen on |

Options combine, for example `--t0 20 --monitor`. All values are 0-4095 except where noted.

### Reading `--monitor` output

Not every line is a pad you pressed. If you see pads you didn't hit:

- **`NOT A PAD` lines** are note messages from touching an encoder or the touch strip, which the Push sends the same way as pads. Pads are notes 36-99; anything else is something else. These are normal.
- **Very low velocities (1-5)** are real but usually inaudible, so a pad can show up here without making sound.
- **Neighboring pads** can pick up a light touch when you press the pad next to them, which shows up as a low velocity.
- **A low `--t0`** makes ghost triggers more likely. If they appear while testing it, run `--reset` and check whether they stop.

The app only prints messages the Push actually sends; it doesn't create or guess at hits.

### Experimental: trigger on a lighter touch

*Untested and may not work.*

Live's own Push 2 script sends two hardcoded values (`33` and `31`) in a pad parameter command that Ableton's docs label "unused". They may control how light a touch triggers a pad. To try lowering them:

    ./venv/bin/python push2_pad_fix.py --t0 20 --monitor

Try a very light tap. If it triggers more easily, lower `--t0` further until pads start sticking or firing by themselves, then back off. To check the value does anything at all, try a high one like `--t0 150` once; pads should get harder to trigger. If pads stick, run `--reset` or power-cycle the Push.

Live re-sends its own values when you change Sensitivity, Gain or Dynamics on the Push, or reconnect it, so keep the app running for the override to hold.

### How it works

- On start, after mode-change messages from the Push, and on a timer, it sends the documented "Select Pad Settings" sysex (command `0x28`) for all pads.
- With `--t0`, it also sends "Set Pad Parameters" (command `0x1B`).
- Reference: [Ableton's Push 2 MIDI and Display Interface](https://github.com/Ableton/push-interface/blob/main/doc/AbletonPush2MIDIDisplayInterface.asc).

## Credits

Based on [BenDS1984/push2-pad-sensitivity](https://github.com/BenDS1984/push2-pad-sensitivity), reworked for macOS. Created with the help of AI ([Claude](https://claude.ai) by Anthropic).
