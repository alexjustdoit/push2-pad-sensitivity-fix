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
- **Pads still feel stiff in every mode**: this app can only hold the "regular" setting, the most sensitive of the three that Push 2 offers. See the experimental section below.

---

## Experimental: trigger on a lighter touch

*Optional and for people comfortable in Terminal. This is untested and may not work.*

Live's own Push 2 script sends two hardcoded values (`33` and `31`) in a pad parameter command that Ableton's docs label "unused". They may control how light a touch triggers a pad. This app can override them:

    ./venv/bin/python push2_pad_fix.py --t0 20 --monitor    # t1 defaults to t0 minus 2; --monitor prints each pad hit
    ./venv/bin/python push2_pad_fix.py --reset              # back to Live's 33/31

Try a very light tap. If it triggers more easily, lower `--t0` further until pads start sticking or firing by themselves, then back off. If pads stick, run `--reset` or power-cycle the Push. Live re-sends its own values when you change Sensitivity, Gain or Dynamics on the Push, so keep the app running.

Other options: `--list` shows MIDI ports, `--setting 1` or `2` picks a less sensitive preset, `--interval` sets how often it re-applies (seconds, 0 disables), and `--cpmin` / `--cpmax` set the aftertouch range sent with `--t0` (defaults match Live's middle Sensitivity).

## Credits

Based on [BenDS1984/push2-pad-sensitivity](https://github.com/BenDS1984/push2-pad-sensitivity), reworked for macOS. Created with the help of AI ([Claude](https://claude.ai) by Anthropic).
