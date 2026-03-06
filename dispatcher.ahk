; ─── FlowVim Dispatcher (AutoHotkey v1) ───
; Called by FlowVim plugin: AutoHotkey.exe dispatcher.ahk <command>
; Sends keystroke to the previously-active window after Flow hides.

#NoTrayIcon
#SingleInstance Force
#NoEnv
SetBatchLines, -1
SendMode Input

; ── Read command argument ──
cmd = %1%
if (cmd = "")
    ExitApp

; ── Wait for Flow Launcher to hide and restore focus ──
Sleep, 150

; ── Browser commands ──
if (cmd = "b_next")
    Send, ^{Tab}
else if (cmd = "b_prev")
    Send, ^+{Tab}
else if (cmd = "b_close")
    Send, ^w
else if (cmd = "b_reopen")
    Send, ^+t
else if (cmd = "b_new")
    Send, ^t
else if (cmd = "b_addr")
    Send, ^l
else if (cmd = "b_full")
    Send, {F11}
else if (cmd = "b_left")
    Send, ^+{PgUp}
else if (cmd = "b_right")
    Send, ^+{PgDn}
else if (cmd = "b_dev")
    Send, {F12}
else if (cmd = "b_incog")
    Send, ^+n
else if (cmd = "b_dup")
{
    ; Duplicate tab: focus address bar, select URL, open in new tab
    Send, ^l
    Sleep, 50
    Send, !{Enter}
}
else if (cmd = "b_pin")
{
    ; Pin tab via keyboard: no universal shortcut, simulate right-click menu
    ; Works in Chrome/Edge: right-click tab, then P for pin
    Send, {AppsKey}
    Sleep, 100
    Send, p
}
else if (cmd = "b_tab1")
    Send, ^1
else if (cmd = "b_tab2")
    Send, ^2
else if (cmd = "b_tab3")
    Send, ^3
else if (cmd = "b_tab4")
    Send, ^4
else if (cmd = "b_tab5")
    Send, ^5
else if (cmd = "b_tab6")
    Send, ^6
else if (cmd = "b_tab7")
    Send, ^7
else if (cmd = "b_tab8")
    Send, ^8
else if (cmd = "b_tab9")
    Send, ^9

; ── Window commands ──
else if (cmd = "w_min")
    WinMinimize, A
else if (cmd = "w_max")
{
    ; Toggle maximize: if maximized, restore; otherwise maximize
    WinGet, state, MinMax, A
    if (state = 1)
        WinRestore, A
    else
        WinMaximize, A
}
else if (cmd = "w_close")
    Send, !{F4}
else if (cmd = "w_left")
    Send, #{Left}
else if (cmd = "w_right")
    Send, #{Right}

; ── Screen commands ──
else if (cmd = "s_snip")
    Send, #+s
else if (cmd = "s_proj")
    Send, #p
else if (cmd = "s_disp")
    Run, ms-settings:display

; ── Text editing commands ──
else if (cmd = "t_all")
    Send, ^a
else if (cmd = "t_line")
{
    ; Select current line: Home then Shift+End
    Send, {Home}
    Sleep, 20
    Send, +{End}
}
else if (cmd = "t_dline")
{
    ; Delete current line: Home, Shift+End, Delete
    Send, {Home}
    Sleep, 20
    Send, +{End}
    Sleep, 20
    Send, {Delete}
}
else if (cmd = "t_word")
{
    ; Select word under cursor: Ctrl+Shift+Left (selects word to the left)
    Send, ^+{Left}
}
else if (cmd = "t_dword")
    Send, ^{Backspace}
else if (cmd = "t_home")
    Send, {Home}
else if (cmd = "t_end")
    Send, {End}
else if (cmd = "t_top")
    Send, ^{Home}
else if (cmd = "t_bottom")
    Send, ^{End}
else if (cmd = "t_shome")
    Send, +{Home}
else if (cmd = "t_send")
    Send, +{End}
else if (cmd = "t_stop")
    Send, ^+{Home}
else if (cmd = "t_sbot")
    Send, ^+{End}
else if (cmd = "t_sword")
    Send, ^+{Left}
else if (cmd = "t_swordr")
    Send, ^+{Right}
else if (cmd = "t_undo")
    Send, ^z
else if (cmd = "t_redo")
    Send, ^y

; ── Clipboard commands ──
else if (cmd = "c_hist")
    Send, #v
else if (cmd = "c_plain")
    Send, ^+v

ExitApp
