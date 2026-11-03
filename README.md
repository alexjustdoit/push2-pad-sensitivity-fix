# Push 2 Pad Fix (macOS)

Make the pads on your Ableton Push 2 easier to play in Session and sequencer modes.

**This version is for Mac.** Windows users should use the original project this was forked from: https://github.com/BenDS1984/push2-pad-sensitivity

## The problem

In Session mode and in the step sequencer, Push 2 pads need noticeably more pressure than in Note mode. Live does this on purpose, so you don't trigger clips or steps by accident. If you'd rather have lighter pads, this app overrides it. Live puts the stiffer setting back every time you change modes, so the app keeps running in the background and re-applies yours.

## Pad presets: regular, reduced, low

Push 2 has three built-in pad sensitivity presets, and every pad is always on one of them:

| Preset | Number | Feel |
|---|---|---|
| **Regular** | 0 | Most sensitive. Light touches register. |
| **Reduced** | 1 | Needs more pressure than regular. |
| **Low** | 2 | Needs the most pressure. Hardest to trigger. |

Live's stock behavior, as read from a Push 2 running Live 12:

| Pads | Stock preset |
|---|---|
| Drum and instrument playing pads (including the 64-note layout) | **Regular** |
| Drum step sequencer and loop selector areas | **Low** |
| Session mode (all 64 pads) | **Low** |

So Session and sequencer pads are two steps stiffer than playing pads. Presets are the only pad sensitivity control Push 2 offers for how much pressure it takes to trigger a pad. (Sensitivity, Gain and Dynamics in Push's Setup menu only change how hard a pad *plays* once it triggers.)

## Pick a mode

| Mode | What it does | Launcher |
|---|---|---|
| **Standard** | Puts **every** pad on regular, in every mode. Lightest feel, but nothing is protected from accidental hits. | `Start_Push2_Fix.command` |
| **Protect** | Leaves playing pads on regular, and moves Session and sequencer/loop pads from low to **reduced**. Lighter than stock, but still a bit stiffer than playing pads, so they're harder to hit by accident. | `Start_Push2_Fix_Protect.command` |

If you're not sure, start with **Protect**. If those pads still feel too stiff, switch to **Standard**.

## What you need

- A Mac with Ableton Live 12 and a Push 2 connected by USB
- Python 3, a free download from https://www.python.org/downloads/ (if you're not sure you have it, the launcher will tell you)

## Install

1. Go to the [Releases page](../../releases/latest) and download the **Source code (zip)**.
2. Open the downloaded ZIP to unpack it, and move the folder somewhere permanent, like Documents.

## Use

1. Open Ableton Live with your Push 2 connected.
2. In the folder, double-click the launcher for the mode you picked (see above).
   - The first time, macOS will block it because it's a downloaded file. Click **Done** (don't move it to the Trash), then open **System Settings** (**System Preferences** on older macOS) → **Privacy & Security**, scroll to the bottom, and click **Open Anyway** next to the message about the launcher. Enter your password if asked, then click **Open**. You only need to do this once per launcher.
   - On some older versions of macOS, right-clicking the file and choosing **Open** works instead.
   - The first run sets itself up, which takes about a minute.
3. A Terminal window opens and prints what it's doing. **Leave it open** while you use Ableton. Close the window, or press **Ctrl+C**, to stop it.

Stopping the app doesn't undo anything on the Push. The last presets stay until Live changes them (for example when you switch modes) or you reconnect the Push.

## Troubleshooting

- **"No output port matching 'Push 2 User Port'"**: the Push 2 isn't connected or isn't powered on.
- **Pads still feel stiff in every mode**: this app can only change the preset, and "regular" is the most sensitive one Push 2 has. Pads that feel stiff even on regular are down to the pad hardware, which this app can't change. Take apart your Push and clean the conductive sheet between the pads and the PCB.

---

# Technical details and diagnostics

*Everything below is optional. For people comfortable in Terminal. Run these from the project folder.*

    ./venv/bin/python push2_pad_fix.py [options]

Press **Ctrl+C** to stop.

## Common commands

| Command | What it does |
|---|---|
| `./venv/bin/python push2_pad_fix.py` | Standard mode: every pad on regular |
| `./venv/bin/python push2_pad_fix.py --protect` | Protect mode: step each pad down one preset from what Live set |
| `./venv/bin/python push2_pad_fix.py --dump` | Print a grid of every pad's current preset and exit |
| `./venv/bin/python push2_pad_fix.py --monitor` | Live readout of every pad hit, e.g. `pad 36 (row 1 from bottom, col 1) velocity 18` |
| `./venv/bin/python push2_pad_fix.py --list` | List the MIDI ports the Mac can see, then exit. Use it if the Push isn't found |

## All options

| Option | Default | Meaning |
|---|---|---|
| `--setting 0\|1\|2` | `0` | Preset to apply to every pad in Standard mode: 0 regular, 1 reduced, 2 low |
| `--protect` | off | Step each pad down one preset from what Live set. Can't be combined with `--setting` |
| `--dump` | | Print each pad's current preset as a grid and exit |
| `--monitor` | off | Print each pad note-on (pad number, position and velocity); other touches are labeled `NOT A PAD` |
| `--list` | | Show MIDI ports and exit |
| `--interval S` | `5` | Seconds between background re-applies. `0` turns this off (it then only re-applies on mode changes) |
| `--out NAME` | `Push 2 User Port` | Part of the MIDI output port name to send to |
| `--in NAME` | `Push 2 Live Port` | Part of the MIDI input port name to listen on |
| `--reset` | | Send Live's own values for `--t0`/`--t1` once and exit |
| `--t0 N`, `--t1 N`, `--cpmin N`, `--cpmax N` | off | Experimental pad parameter override (see below) |

Options combine, for example `--protect --monitor`.

## Protect mode in detail

`--protect` reads each pad's current preset and writes one step lower: low becomes reduced, reduced becomes regular, and regular stays regular. It checks every few seconds and after mode changes, and remembers what it wrote so it never steps a pad down twice. It prints each change, e.g. `pad row 8 col 1: low -> reduced`.

Because Live's stock presets are only regular and low (see above), this means playing pads stay regular and everything else goes to reduced.

## Seeing what Live sets in each mode

Switch modes on the Push and run `./venv/bin/python push2_pad_fix.py --dump` (with the app stopped). It prints an 8x8 grid, top row first. Example from a drum mode with the loop selector open (0 = regular, 2 = low):

      2 2 2 2 2 2 2 2
      2 2 2 2 2 2 2 2
      2 2 2 2 2 2 2 2
      2 2 2 2 2 2 2 2
      0 0 0 0 2 2 2 2
      0 0 0 0 2 2 2 2
      0 0 0 0 2 2 2 2
      0 0 0 0 2 2 2 2

## Reading `--monitor` output

Not every line is a pad you pressed. If you see pads you didn't hit:

- **`NOT A PAD` lines** are note messages from touching an encoder or the touch strip, which the Push sends the same way as pads. Pads are notes 36-99; anything else is something else. These are normal.
- **Very low velocities (1-5)** are real but usually inaudible, so a pad can show up here without making sound.
- **Neighboring pads** can pick up a light touch when you press the pad next to them, which shows up as a low velocity.

The app only prints messages the Push actually sends; it doesn't create or guess at hits.

## Experimental: pad parameters `--t0` / `--t1`

*Didn't work in testing. Left in for anyone who wants to experiment.*

Live's Push 2 script sends two hardcoded values (`33` and `31`) in a pad parameter command that Ableton's docs label "unused". I guessed they might be a trigger threshold. Overriding them (`--t0 20`, `--t0 150`) made no noticeable difference to how pads trigger, so they don't appear to control it. `--reset` sends Live's own values (33/31) back.

## How it works

- Standard mode sends the documented "Select Pad Settings" sysex (command `0x28`) for all pads at start, after mode-change messages from the Push, and on a timer.
- `--protect` first reads each pad's preset with "Get Selected Pad Settings" (`0x29`), then sets it one step lower per pad.
- `--t0` also sends "Set Pad Parameters" (`0x1B`).
- Reference: [Ableton's Push 2 MIDI and Display Interface](https://github.com/Ableton/push-interface/blob/main/doc/AbletonPush2MIDIDisplayInterface.asc).

## Credits

Based on [BenDS1984/push2-pad-sensitivity](https://github.com/BenDS1984/push2-pad-sensitivity), reworked for macOS. Created with the help of AI ([Claude](https://claude.ai) by Anthropic).
