import ctypes
import time
import win32gui
if __name__ == "__main__":
    time.sleep(2)
    w = win32gui
    title = w.GetWindowText (w.GetForegroundWindow())
    print(title)
    import pdb; pdb.set_trace()
    # handle = ctypes.windll.user32.FindWindowW(0, "FINAL FANTASY XIV")
    # print(hex(handle))
    # WM_CHAR = 0x0102
    # ctypes.windll.user32.SendMessageW(0x000205F8, WM_CHAR, 0x61, 0)