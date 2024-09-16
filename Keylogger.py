from ctypes import *
from ctypes import wintypes

"""
hooks in Win32API are used to monitor and respond events such as messages, keystrokes, mouseactions etc...
"""

#defining constants
user32 = windll.user32
LRESULT = c_long
WH_KEYBOARD_LL = 13 #installs the hook procedure to monitor
WM_KEYDOWN = 0x0100 #A nonsystem key is a key that is pressed when the ALT key is not pressed.
WM_RETURN = 0X0D
WM_SHIFT = 0X10


# this GetWindowTextLengthA API is used to get the length of the text associated with the window A denotes return the output as unicode
# GetWindowTextLenthW returns the output in the unicode format
GetWindowTextLengthA = user32.GetWindowTextLengthA
GetWindowTextLengthA.argtypes=(wintypes.HANDLE, )
GetWindowTextLengthA.restype = wintypes.INT


#GetWindowTextA function used to retrieve the text associated with the comtrol bars such as the windows, buttons , edit box 'A' denotes the output is ANSI
GetWindowTextA = user32.GetWindowTextA
GetWindowTextA.argtypes = (wintypes.HANDLE, wintypes.LPSTR, wintypes.INT)
GetWindowTextA.restype = wintypes.INT 

#GetKeyState function is used to retrive the status of the virtual space of the keyboard whether the key is pressed or toggled
GetKeyState = user32.GetKeyState
GetKeyState.argtypes = (wintypes.INT, )
GetKeyState.restype = wintypes.SHORT

#GetKeyboardState function is used to copy and the status of the 256 vitual key to specified buffer
KeyboardState = wintypes.PBYTE * 256
GetKeyboardState = user32.GetKeyboardState
GetKeyboardState.argtypes = (POINTER(KeyboardState), )
GetKeyboardState.restype = wintypes.BOOL

#ToAscii function converts the virtual keycode and keyboard state to corresponding characters
ToAscii = user32.ToAscii
ToAscii.argtypes = (wintypes.UINT, wintypes.UINT, POINTER(KeyboardState), wintypes.LPWORD, wintypes.UINT)
ToAscii.restype = wintypes.INT 

#CallNextHookEx function is used to call the procedure of next hook to current hook chain , this function inturupts the keyboard or the mouse events
CallNextHookEx = user32.CallNextHookEx
CallNextHookEx.argtypes = (wintypes.HHOOK, wintypes.INT, wintypes.WPARAM, wintypes.LPARAM)
CallNextHookEx.restype = LRESULT

#SetWindowsHookExA used to install the certain hook procedure into the hook chain to monitor system for certain events
HOOKPROC = CFUNCTYPE(LRESULT, wintypes.WPARAM, wintypes.LPARAM)
SetWindowsHookExA = user32.SetWindowsHookExA
SetWindowsHookExA.argtypes = (wintypes.INT,HOOKPROC, wintypes.HINSTANCE, wintypes.DWORD)
SetWindowsHookExA.restype = wintypes.HHOOK


#GetMessage function dispatches incoming sent messages until a posted message is available for retrieval.
GetMessage = user32.GetMessageW
GetMessage.argtypes = (wintypes.LPMSG, wintypes.HWND, wintypes.UINT, wintypes.UINT)
GetMessage.restype = wintypes.BOOL


#this structure helps us to identify which key is pressed

class KBDLLHOOKSTRUCT(Structure):
	_fields_ = [("vkCode", wintypes.DWORD),
				("scanCode", wintypes.DWORD),
				("flags", wintypes.DWORD),
				("time", wintypes.DWORD),
				("dwExtraInfo", wintypes.DWORD,)
				]

def get_foreground_process():
	#this function Retrieves a handle to the foreground window (the window with which the user is currently working).
	hwnd = user32.GetForegroundWindow()
	length = GetWindowTextLengthA(hwnd) #gets the length text to understand which is the user currently running
	buf = create_string_buffer(length + 1)
	GetWindowTextA(hwnd, buf, length) #this will copy the text from handle to buffer
	return buf.value

print(get_foreground_process())	