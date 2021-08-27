import time
import win32gui

def is_active():
    w = win32gui
    return w.GetWindowText (w.GetForegroundWindow()) == 'FINAL FANTSY XIV'