# FlowVim

**Stop memorizing keyboard shortcuts. Start typing what you want.**

![Flow Launcher](https://img.shields.io/badge/Flow_Launcher-Plugin-blue)
![AutoHotkey](https://img.shields.io/badge/AutoHotkey-v1-green)
![Python](https://img.shields.io/badge/Python-3.11-yellow)
![Commands](https://img.shields.io/badge/45_Commands-Ready-brightgreen)

---

## The Problem

You know the feeling.

You're deep in a browser with 30 tabs open. You need to close one, snap a window to the left, take a screenshot, and get back to work.

So you reach for the keyboard and... nothing. What was it? `Ctrl+Shift+Tab`? `Win+Left`? `Ctrl+Shift+PgUp`?

You Google it. Again. For the third time this week.

And the "solution" everyone gives you? _Memorize more hotkeys._ Install AutoHotkey. Write scripts. Build muscle memory.

Here's the thing nobody tells you: **you don't need muscle memory if you can just say what you want.**

## The Fix

FlowVim turns [Flow Launcher](https://www.flowlauncher.com/) into a command palette for your entire operating system.

You already know how to type words. So type words:

- `b next` -- next browser tab
- `w min` -- minimize the window
- `e line` -- select the current line
- `c hist` -- open clipboard history

That's it. No modifier keys. No memorization. No cheat sheets taped to your monitor.

Open Flow Launcher. Type two words. Press Enter. Done.

## What You Get

**45 commands** across 4 active categories, all accessible by typing or voice (Win+H).

### Browser (`b`) -- 18 commands

Everything you do with browser tabs, without remembering a single Ctrl+Shift+Something combo.

| Command    | What it does          | The shortcut you'll never need to memorize |
| ---------- | --------------------- | ------------------------------------------ |
| `b next`   | Next tab              | Ctrl+Tab                                   |
| `b prev`   | Previous tab          | Ctrl+Shift+Tab                             |
| `b close`  | Close tab             | Ctrl+W                                     |
| `b reopen` | Reopen closed tab     | Ctrl+Shift+T                               |
| `b new`    | New tab               | Ctrl+T                                     |
| `b addr`   | Focus address bar     | Ctrl+L                                     |
| `b full`   | Toggle fullscreen     | F11                                        |
| `b left`   | Move tab left         | Ctrl+Shift+PgUp                            |
| `b right`  | Move tab right        | Ctrl+Shift+PgDn                            |
| `b dev`    | DevTools              | F12                                        |
| `b incog`  | New incognito window  | Ctrl+Shift+N                               |
| `b dup`    | Duplicate current tab | Ctrl+L then Alt+Enter                      |
| `b pin`    | Pin/unpin tab         | Context menu shortcut                      |
| `b 1`      | Go to tab 1           | Ctrl+1                                     |
| `b 2`      | Go to tab 2           | Ctrl+2                                     |
| ...        | ...                   | ...                                        |
| `b 9`      | Go to last tab        | Ctrl+9                                     |

### Window (`w`) -- 5 commands

Snap, minimize, maximize, close. The window management shortcuts that are slightly different on every OS and impossible to keep straight.

| Command   | What it does                               | The shortcut       |
| --------- | ------------------------------------------ | ------------------ |
| `w min`   | Minimize active window                     | Minimize           |
| `w max`   | Maximize (or restore if already maximized) | Toggle max/restore |
| `w close` | Close window                               | Alt+F4             |
| `w left`  | Snap window to left half                   | Win+Left           |
| `w right` | Snap window to right half                  | Win+Right          |

### Screen (`s`) -- 3 commands (requires setup)

> **Note:** The `s` keyword conflicts with the built-in **Windows Settings** plugin, which also claims `s`. To use FlowVim's screen commands, change the Windows Settings plugin's keyword: Flow Launcher Settings (Ctrl+I) > Plugins > Windows Settings > change action keyword from `s` to `set`. If you don't need screen commands, just skip this.

| Command  | What it does               | The shortcut        |
| -------- | -------------------------- | ------------------- |
| `s snip` | Open snipping tool         | Win+Shift+S         |
| `s proj` | Project/extend screen menu | Win+P               |
| `s disp` | Open display settings      | ms-settings:display |

### Text Edit (`e`) -- 17 commands

This is where it gets interesting. Every text editing action you'd want from vim, but it works in _any_ text field on Windows. Notepad. Chrome. Slack. Anywhere.

| Command    | What it does                | The shortcut            |
| ---------- | --------------------------- | ----------------------- |
| `e all`    | Select all                  | Ctrl+A                  |
| `e line`   | Select current line         | Home then Shift+End     |
| `e dline`  | Delete current line         | Home, Shift+End, Delete |
| `e word`   | Select word                 | Ctrl+Shift+Left         |
| `e dword`  | Delete word backwards       | Ctrl+Backspace          |
| `e home`   | Jump to start of line       | Home                    |
| `e end`    | Jump to end of line         | End                     |
| `e top`    | Jump to start of document   | Ctrl+Home               |
| `e bottom` | Jump to end of document     | Ctrl+End                |
| `e shome`  | Select to start of line     | Shift+Home              |
| `e send`   | Select to end of line       | Shift+End               |
| `e stop`   | Select to start of document | Ctrl+Shift+Home         |
| `e sbot`   | Select to end of document   | Ctrl+Shift+End          |
| `e sword`  | Select word left            | Ctrl+Shift+Left         |
| `e swordr` | Select word right           | Ctrl+Shift+Right        |
| `e undo`   | Undo                        | Ctrl+Z                  |
| `e redo`   | Redo                        | Ctrl+Y                  |

### Clipboard (`c`) -- 2 commands

Small category. Massive value. Especially `c plain` -- if you've ever pasted text from a website and watched it explode your document's formatting, this one's for you.

| Command   | What it does                        | The shortcut |
| --------- | ----------------------------------- | ------------ |
| `c hist`  | Open clipboard history              | Win+V        |
| `c plain` | Paste as plain text (no formatting) | Ctrl+Shift+V |

---

## How It Actually Works

No magic. No cloud. No telemetry. Three files and a very simple idea.

```
You type "b next"
       |
       v
Flow Launcher sees keyword "b", calls main.py with query "next"
       |
       v
main.py searches its command list, returns "Browser: Next Tab (Ctrl+Tab)"
       |
       v
You press Enter
       |
       v
main.py launches: AutoHotkey.exe dispatcher.ahk b_next
       |
       v
dispatcher.ahk waits 150ms for Flow to hide, then sends Ctrl+Tab
       |
       v
Your browser switches to the next tab. You never left the keyboard.
```

### The files

```
FlowVim-1.0.0/
  plugin.json       -- Tells Flow Launcher: "I handle keywords b, w, s, e, c"
  main.py           -- Python. Searches commands, returns results. Zero dependencies.
  dispatcher.ahk    -- AutoHotkey v1. Receives a command ID, sends the keystroke.
  Images/icon.png   -- Plugin icon
```

**Zero external Python dependencies.** The plugin implements the Flow Launcher JSON-RPC protocol from scratch in ~100 lines. No pip install. No virtualenv. No package conflicts. It just works.

**Why AutoHotkey?** Because sending keystrokes on Windows is surprisingly hard to get right. AutoHotkey has spent 20 years solving edge cases around focus management, key timing, and modifier states. We use that instead of reinventing it.

**Why the 150ms delay?** When you press Enter in Flow Launcher, it starts hiding. But if AutoHotkey sends the keystroke immediately, it goes to Flow Launcher instead of your app. The 150ms wait lets Flow finish hiding and your previous window regain focus. Reliable on every machine we've tested.

---

## Installation

### What you need

1. **[Flow Launcher](https://www.flowlauncher.com/)** -- tested on v2.1.0, should work on any recent version
2. **[AutoHotkey v1](https://www.autohotkey.com/)** -- the classic version, not v2. Installed at `C:\Program Files\AutoHotkey\`

### Setup (2 minutes)

**Option A: Clone from GitHub**

```bash
cd %APPDATA%\FlowLauncher\Plugins
git clone https://github.com/yaronbeen/FlowVim.git FlowVim-1.0.0
```

**Option B: Download ZIP**

1. Download this repo as a ZIP
2. Extract to `%APPDATA%\FlowLauncher\Plugins\FlowVim-1.0.0\`

**Then:**

3. Restart Flow Launcher (right-click the tray icon > Restart)
4. Type `b next` -- you should see "Browser: Next Tab"
5. Press Enter -- your browser should switch tabs

If it doesn't work, check:

- Is AutoHotkey v1 installed at `C:\Program Files\AutoHotkey\AutoHotkey.exe`?
- Did you restart Flow Launcher (not just close and reopen the search bar)?

### Custom AutoHotkey path

If your AutoHotkey is installed somewhere else, edit one line in `main.py`:

```python
AHK_EXE = r"C:\Program Files\AutoHotkey\AutoHotkey.exe"  # change this
```

### Voice typing (Win+H)

FlowVim registers both lowercase and uppercase variants of every keyword (`b` and `B`, `e` and `E`, etc.). Windows voice typing capitalizes the first letter, so saying "B next" or "b next" both work. Note that `s`/`S` may not work if the Windows Settings plugin claims that keyword first (see Screen section above).

---

## Bonus: CapsLock Navigation Layer

Not part of the plugin, but the perfect companion. A standalone AutoHotkey script that turns CapsLock into a navigation modifier:

| Combo            | Action                          |
| ---------------- | ------------------------------- |
| CapsLock + W     | Up arrow                        |
| CapsLock + A     | Left arrow                      |
| CapsLock + S     | Down arrow                      |
| CapsLock + D     | Right arrow                     |
| CapsLock + Q     | Home                            |
| CapsLock + E     | End                             |
| CapsLock + R     | Page Up                         |
| CapsLock + F     | Page Down                       |
| CapsLock + X     | Delete                          |
| Shift + CapsLock | Toggle caps lock (escape hatch) |

Save this as a `.ahk` file and drop it in `shell:startup` to run on boot:

```autohotkey
#NoEnv
#SingleInstance Force
SetBatchLines, -1
SendMode Input

CapsLock & w::Send, {Up}
CapsLock & a::Send, {Left}
CapsLock & s::Send, {Down}
CapsLock & d::Send, {Right}
CapsLock & q::Send, {Home}
CapsLock & e::Send, {End}
CapsLock & r::Send, {PgUp}
CapsLock & f::Send, {PgDn}
CapsLock & x::Send, {Delete}

+CapsLock::
    SetCapsLockState, % GetKeyState("CapsLock", "T") ? "Off" : "On"
return

CapsLock::return
```

---

## Adding Your Own Commands

The whole point of this plugin is that it's dead simple to extend.

**Step 1:** Open `main.py`, find the `COMMANDS` list, add your command:

```python
{"key": "mute", "cat": "Media", "title": "Mute Volume", "sub": "Toggle mute", "cmd": "m_mute"},
```

**Step 2:** Open `dispatcher.ahk`, add the handler:

```autohotkey
else if (cmd = "m_mute")
    Send, {Volume_Mute}
```

**Step 3:** If you added a new category, add the keyword to `plugin.json`:

```json
"ActionKeywords": ["b", "B", "w", "W", "s", "S", "e", "E", "c", "C", "m", "M"],
```

**Step 4:** Restart Flow Launcher. Your new command is live.

That's it. No build step. No compilation. No deployment pipeline. Edit two files and restart.

---

## FAQ

**Does this work with Firefox/Edge/Brave?**
Yes. The browser commands send standard keyboard shortcuts (Ctrl+Tab, Ctrl+W, etc.) that work in every Chromium and Firefox-based browser. The only exception is `b pin` which uses Chrome/Edge's context menu shortcut.

**Does this conflict with other Flow Launcher plugins?**
Flow Launcher allows only one plugin per action keyword. FlowVim registers `b`, `w`, `e`, `c` (plus uppercase variants `B`, `W`, `E`, `C` for voice typing). The `s` keyword may conflict with the built-in Windows Settings plugin -- see the Screen section for the fix. Keywords `b`, `w`, `e`, `c` have no conflicts with default plugins.

**Why not just use AutoHotkey directly?**
You could. But then you need to memorize a bunch of hotkey combos -- which is the exact problem we're solving. FlowVim gives you a searchable, discoverable interface. You type what you want in plain English.

**Why Python and not C#?**
Python plugins are easier to hack on. You can edit `main.py` in Notepad and restart Flow Launcher. No Visual Studio, no compilation, no NuGet packages. The tradeoff is ~100ms startup time per query, but since Python only launches when you type one of our 5 keywords, you'll never notice.

**Can I change the keywords?**
Yes. Edit `plugin.json` and change the `ActionKeywords` array. Then restart Flow Launcher. You can use any single character or short string that doesn't conflict with your other plugins.

**Does this work with voice typing (Win+H)?**
Yes. The plugin registers uppercase variants of every keyword. Windows voice typing capitalizes the first letter, so saying "B next" produces `B next` which triggers FlowVim. The only exception is `s`/`S` if the Windows Settings plugin is claiming that keyword.

---

## License

MIT. Do whatever you want with it.
