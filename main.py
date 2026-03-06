# -*- coding: utf-8 -*-
"""
FlowVim - Vim-like command palette for Flow Launcher.

Bare JSON-RPC implementation (no external dependencies).
Registers keywords: b (browser), w (window), s (screen), t (text), c (clipboard).

NOTE: Flow Launcher strips the action keyword before calling query(),
so we cannot distinguish which keyword (b/w/s) triggered the call.
We search ALL commands and show category labels in titles.
For the 3 overlapping names (close, left, right), both results appear.
"""

import json
import sys
import os
import subprocess

# ── Command Registry ──────────────────────────────────────────────
# Each command: key (what user types), cat (category label),
# title (display name), sub (subtitle/shortcut hint), cmd (dispatcher arg)

COMMANDS = [
    # ── Browser (keyword: b) ──
    {
        "key": "next",
        "cat": "Browser",
        "title": "Next Tab",
        "sub": "Ctrl+Tab",
        "cmd": "b_next",
    },
    {
        "key": "prev",
        "cat": "Browser",
        "title": "Previous Tab",
        "sub": "Ctrl+Shift+Tab",
        "cmd": "b_prev",
    },
    {
        "key": "close",
        "cat": "Browser",
        "title": "Close Tab",
        "sub": "Ctrl+W",
        "cmd": "b_close",
    },
    {
        "key": "reopen",
        "cat": "Browser",
        "title": "Reopen Closed Tab",
        "sub": "Ctrl+Shift+T",
        "cmd": "b_reopen",
    },
    {
        "key": "new",
        "cat": "Browser",
        "title": "New Tab",
        "sub": "Ctrl+T",
        "cmd": "b_new",
    },
    {
        "key": "addr",
        "cat": "Browser",
        "title": "Focus Address Bar",
        "sub": "Ctrl+L",
        "cmd": "b_addr",
    },
    {
        "key": "full",
        "cat": "Browser",
        "title": "Toggle Fullscreen",
        "sub": "F11",
        "cmd": "b_full",
    },
    {
        "key": "left",
        "cat": "Browser",
        "title": "Move Tab Left",
        "sub": "Ctrl+Shift+PgUp",
        "cmd": "b_left",
    },
    {
        "key": "right",
        "cat": "Browser",
        "title": "Move Tab Right",
        "sub": "Ctrl+Shift+PgDn",
        "cmd": "b_right",
    },
    {
        "key": "dev",
        "cat": "Browser",
        "title": "DevTools",
        "sub": "F12",
        "cmd": "b_dev",
    },
    {
        "key": "incog",
        "cat": "Browser",
        "title": "New Incognito Window",
        "sub": "Ctrl+Shift+N",
        "cmd": "b_incog",
    },
    {
        "key": "dup",
        "cat": "Browser",
        "title": "Duplicate Tab",
        "sub": "Alt+D then Alt+Enter",
        "cmd": "b_dup",
    },
    {
        "key": "pin",
        "cat": "Browser",
        "title": "Pin/Unpin Tab",
        "sub": "Right-click menu",
        "cmd": "b_pin",
    },
    {
        "key": "1",
        "cat": "Browser",
        "title": "Go to Tab 1",
        "sub": "Ctrl+1",
        "cmd": "b_tab1",
    },
    {
        "key": "2",
        "cat": "Browser",
        "title": "Go to Tab 2",
        "sub": "Ctrl+2",
        "cmd": "b_tab2",
    },
    {
        "key": "3",
        "cat": "Browser",
        "title": "Go to Tab 3",
        "sub": "Ctrl+3",
        "cmd": "b_tab3",
    },
    {
        "key": "4",
        "cat": "Browser",
        "title": "Go to Tab 4",
        "sub": "Ctrl+4",
        "cmd": "b_tab4",
    },
    {
        "key": "5",
        "cat": "Browser",
        "title": "Go to Tab 5",
        "sub": "Ctrl+5",
        "cmd": "b_tab5",
    },
    {
        "key": "6",
        "cat": "Browser",
        "title": "Go to Tab 6",
        "sub": "Ctrl+6",
        "cmd": "b_tab6",
    },
    {
        "key": "7",
        "cat": "Browser",
        "title": "Go to Tab 7",
        "sub": "Ctrl+7",
        "cmd": "b_tab7",
    },
    {
        "key": "8",
        "cat": "Browser",
        "title": "Go to Tab 8",
        "sub": "Ctrl+8",
        "cmd": "b_tab8",
    },
    {
        "key": "9",
        "cat": "Browser",
        "title": "Go to Last Tab",
        "sub": "Ctrl+9",
        "cmd": "b_tab9",
    },
    # ── Window (keyword: w) ──
    {
        "key": "min",
        "cat": "Window",
        "title": "Minimize Window",
        "sub": "Minimize active",
        "cmd": "w_min",
    },
    {
        "key": "max",
        "cat": "Window",
        "title": "Maximize Window",
        "sub": "Toggle maximize/restore",
        "cmd": "w_max",
    },
    {
        "key": "close",
        "cat": "Window",
        "title": "Close Window",
        "sub": "Alt+F4",
        "cmd": "w_close",
    },
    {
        "key": "left",
        "cat": "Window",
        "title": "Snap Window Left",
        "sub": "Win+Left",
        "cmd": "w_left",
    },
    {
        "key": "right",
        "cat": "Window",
        "title": "Snap Window Right",
        "sub": "Win+Right",
        "cmd": "w_right",
    },
    # ── Screen (keyword: s) ──
    {
        "key": "snip",
        "cat": "Screen",
        "title": "Snipping Tool",
        "sub": "Win+Shift+S",
        "cmd": "s_snip",
    },
    {
        "key": "proj",
        "cat": "Screen",
        "title": "Project / Extend",
        "sub": "Win+P",
        "cmd": "s_proj",
    },
    {
        "key": "disp",
        "cat": "Screen",
        "title": "Display Settings",
        "sub": "Opens display settings",
        "cmd": "s_disp",
    },
    # ── Text editing (keyword: t) ──
    {
        "key": "all",
        "cat": "Text",
        "title": "Select All",
        "sub": "Ctrl+A",
        "cmd": "t_all",
    },
    {
        "key": "line",
        "cat": "Text",
        "title": "Select Line",
        "sub": "Home, Shift+End",
        "cmd": "t_line",
    },
    {
        "key": "dline",
        "cat": "Text",
        "title": "Delete Line",
        "sub": "Home, Shift+End, Delete",
        "cmd": "t_dline",
    },
    {
        "key": "word",
        "cat": "Text",
        "title": "Select Word",
        "sub": "Ctrl+Shift+Left or double-click",
        "cmd": "t_word",
    },
    {
        "key": "dword",
        "cat": "Text",
        "title": "Delete Word",
        "sub": "Ctrl+Backspace",
        "cmd": "t_dword",
    },
    {
        "key": "home",
        "cat": "Text",
        "title": "Jump to Start of Line",
        "sub": "Home",
        "cmd": "t_home",
    },
    {
        "key": "end",
        "cat": "Text",
        "title": "Jump to End of Line",
        "sub": "End",
        "cmd": "t_end",
    },
    {
        "key": "top",
        "cat": "Text",
        "title": "Jump to Start of Document",
        "sub": "Ctrl+Home",
        "cmd": "t_top",
    },
    {
        "key": "bottom",
        "cat": "Text",
        "title": "Jump to End of Document",
        "sub": "Ctrl+End",
        "cmd": "t_bottom",
    },
    {
        "key": "shome",
        "cat": "Text",
        "title": "Select to Start of Line",
        "sub": "Shift+Home",
        "cmd": "t_shome",
    },
    {
        "key": "send",
        "cat": "Text",
        "title": "Select to End of Line",
        "sub": "Shift+End",
        "cmd": "t_send",
    },
    {
        "key": "stop",
        "cat": "Text",
        "title": "Select to Start of Document",
        "sub": "Ctrl+Shift+Home",
        "cmd": "t_stop",
    },
    {
        "key": "sbot",
        "cat": "Text",
        "title": "Select to End of Document",
        "sub": "Ctrl+Shift+End",
        "cmd": "t_sbot",
    },
    {
        "key": "sword",
        "cat": "Text",
        "title": "Select Word Left",
        "sub": "Ctrl+Shift+Left",
        "cmd": "t_sword",
    },
    {
        "key": "swordr",
        "cat": "Text",
        "title": "Select Word Right",
        "sub": "Ctrl+Shift+Right",
        "cmd": "t_swordr",
    },
    {
        "key": "undo",
        "cat": "Text",
        "title": "Undo",
        "sub": "Ctrl+Z",
        "cmd": "t_undo",
    },
    {
        "key": "redo",
        "cat": "Text",
        "title": "Redo",
        "sub": "Ctrl+Y",
        "cmd": "t_redo",
    },
    # ── Clipboard (keyword: c) ──
    {
        "key": "hist",
        "cat": "Clipboard",
        "title": "Clipboard History",
        "sub": "Win+V",
        "cmd": "c_hist",
    },
    {
        "key": "plain",
        "cat": "Clipboard",
        "title": "Paste as Plain Text",
        "sub": "Ctrl+Shift+V",
        "cmd": "c_plain",
    },
]

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
ICON = "Images\\icon.png"
AHK_EXE = r"C:\Program Files\AutoHotkey\AutoHotkey.exe"
DISPATCHER = os.path.join(PLUGIN_DIR, "dispatcher.ahk")


def query(q):
    """Return matching commands for the query string."""
    q = q.strip().lower()
    results = []

    for cmd in COMMANDS:
        if q:
            # Match: key starts with query OR query is substring of title
            key_match = cmd["key"].startswith(q)
            title_match = q in cmd["title"].lower()
            if not (key_match or title_match):
                continue

        results.append(
            {
                "Title": "{}: {}".format(cmd["cat"], cmd["title"]),
                "SubTitle": cmd["sub"],
                "IcoPath": ICON,
                "JsonRPCAction": {"method": "run_command", "parameters": [cmd["cmd"]]},
            }
        )

    return results


def run_command(cmd_key):
    """Launch dispatcher.ahk with the command key."""
    # CREATE_NO_WINDOW = 0x08000000 (no console flash)
    subprocess.Popen([AHK_EXE, DISPATCHER, cmd_key], creationflags=0x08000000)


def main():
    """Minimal JSON-RPC handler for Flow Launcher."""
    if len(sys.argv) < 2:
        print(json.dumps({"result": []}))
        return

    try:
        request = json.loads(sys.argv[1])
    except (json.JSONDecodeError, IndexError):
        print(json.dumps({"result": []}))
        return

    method = request.get("method", "")
    params = request.get("parameters", [])

    if method == "query":
        result = query(*params)
    elif method == "run_command":
        run_command(*params)
        result = []
    else:
        result = []

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
