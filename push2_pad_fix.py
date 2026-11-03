#!/usr/bin/env python3
"""Keep Push 2 pads on their most sensitive pad setting (macOS/Windows/Linux).

Ableton Live re-selects pad settings when Push 2 changes mode, which can leave
pads in a stiffer "reduced"/"low" sensitivity. This script sends the documented
"Select Pad Settings" sysex (0x28) for all pads at startup, after mode-change
messages, and on a slow timer as a fallback.

Sysex reference: Ableton push-interface, AbletonPush2MIDIDisplayInterface.asc,
"Pad Settings". Only documented commands are used.
"""
import argparse
import sys
import time

import mido

SYSEX_HEADER = [0x00, 0x21, 0x1D, 0x01, 0x01]  # Ableton ID + Push 2 + device
SELECT_PAD_SETTINGS = 0x28
SET_PAD_PARAMETERS = 0x1B
# Values Live's own Push 2 script sends (Push2/pad_velocity_curve.py): t0/t1 are
# hardcoded, the aftertouch range depends on Live's Sensitivity (this is index 5).
LIVE_T0, LIVE_T1 = 33, 31
LIVE_CPMIN, LIVE_CPMAX = 1220, 1570
LABELS = ["regular", "reduced", "low"]

# Controls whose release (value 0) and pitch-bend reset mark a mode change.
# Taken from BenDS1984/push2-pad-sensitivity.
RESET_CONTROLS = {50, 51, 31, 52, 53, 47, 27, 118, 102, 21, 85}


def find_port(names, needle):
    matches = [n for n in names if needle.lower() in n.lower()]
    return matches[0] if matches else None


def to_7l5m(value):
    return [value & 0x7F, (value >> 7) & 0x1F]


def apply_thresholds(out_port, t0, t1, cpmin, cpmax):
    data = SYSEX_HEADER + [SET_PAD_PARAMETERS] + sum((to_7l5m(v) for v in (t0, t1, cpmin, cpmax)), [])
    out_port.send(mido.Message("sysex", data=data))


def describe_note(msg):
    # Pads are notes 36-99 (36 = bottom left); other note-ons are encoder/touch strip touches.
    if 36 <= msg.note <= 99:
        row, col = divmod(msg.note - 36, 8)
        return f"  pad {msg.note} (row {row + 1} from bottom, col {col + 1}) velocity {msg.velocity}"
    return f"  NOT A PAD: note {msg.note} (encoder or touch strip touch) value {msg.velocity}"


def apply(out_port, setting, quiet=False):
    # scene 0, track 0 = all pads
    out_port.send(mido.Message("sysex", data=SYSEX_HEADER + [SELECT_PAD_SETTINGS, 0, 0, setting]))
    if not quiet:
        print(f"[{time.strftime('%H:%M:%S')}] pad setting -> {LABELS[setting]}", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--setting", type=int, choices=[0, 1, 2], default=0,
                    help="0=regular (most sensitive, default), 1=reduced, 2=low")
    ap.add_argument("--out", default="Push 2 User Port", help="substring of the output port name")
    ap.add_argument("--in", dest="inp", default="Push 2 Live Port", help="substring of the input port name")
    ap.add_argument("--interval", type=float, default=5.0,
                    help="seconds between fallback re-applies (0 disables)")
    ap.add_argument("--list", action="store_true", help="list MIDI ports and exit")
    ap.add_argument("--t0", type=int, help=f"EXPERIMENTAL pad parameter 0 (Live sends {LIVE_T0}); lower may trigger on lighter touch")
    ap.add_argument("--t1", type=int, help=f"EXPERIMENTAL pad parameter 1 (Live sends {LIVE_T1}); default t0-2")
    ap.add_argument("--cpmin", type=int, default=LIVE_CPMIN, help="aftertouch lower threshold, resent with --t0")
    ap.add_argument("--cpmax", type=int, default=LIVE_CPMAX, help="aftertouch upper threshold, resent with --t0")
    ap.add_argument("--reset", action="store_true", help=f"send Live's own t0/t1 ({LIVE_T0}/{LIVE_T1}) once and exit")
    ap.add_argument("--monitor", action="store_true", help="print pad note-ons (to find the lightest touch that triggers)")
    args = ap.parse_args()

    outs, ins = mido.get_output_names(), mido.get_input_names()
    if args.list:
        print("Outputs:", *outs, sep="\n  ")
        print("Inputs:", *ins, sep="\n  ")
        return 0

    if args.reset:
        args.t0, args.t1, args.cpmin, args.cpmax = LIVE_T0, LIVE_T1, LIVE_CPMIN, LIVE_CPMAX
    if args.t0 is not None:
        if args.t1 is None:
            args.t1 = max(args.t0 - 2, 0)
        if not (0 <= args.t1 <= args.t0 <= 4095 and 400 < args.cpmin < args.cpmax <= 4095):
            print("Need 0 <= t1 <= t0 <= 4095 and 400 < cpmin < cpmax <= 4095.", file=sys.stderr)
            return 1

    out_name, in_name = find_port(outs, args.out), find_port(ins, args.inp)
    if not out_name:
        print(f"No output port matching '{args.out}'. Is Push 2 connected? Try --list.", file=sys.stderr)
        return 1
    print(f"Output: {out_name}\nInput:  {in_name or '(none; timer only)'}", flush=True)

    def apply_all(out_port, quiet=False):
        apply(out_port, args.setting, quiet)
        if args.t0 is not None:
            apply_thresholds(out_port, args.t0, args.t1, args.cpmin, args.cpmax)
            if not quiet:
                print(f"[{time.strftime('%H:%M:%S')}] pad parameters -> t0={args.t0} t1={args.t1}", flush=True)

    with mido.open_output(out_name) as out_port:
        if args.reset:
            apply_all(out_port)
            return 0
        apply_all(out_port)
        in_port = mido.open_input(in_name) if in_name else None
        next_tick = time.monotonic() + args.interval
        try:
            while True:
                due = None
                if in_port:
                    for msg in in_port.iter_pending():
                        if args.monitor and msg.type == "note_on" and msg.velocity > 0:
                            print(describe_note(msg), flush=True)
                        if (msg.type == "control_change" and msg.control in RESET_CONTROLS and msg.value == 0):
                            due = 0.15
                        elif msg.type == "pitchwheel" and msg.pitch == 0:
                            due = 0.3
                if due is not None:
                    time.sleep(due)
                    apply_all(out_port)
                elif args.interval and time.monotonic() >= next_tick:
                    apply_all(out_port, quiet=True)
                if args.interval and (due is not None or time.monotonic() >= next_tick):
                    next_tick = time.monotonic() + args.interval
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("\nStopped.")
        finally:
            if in_port:
                in_port.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
