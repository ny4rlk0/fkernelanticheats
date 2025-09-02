import socket
from time import sleep
import time
#from pynput.mouse import Listener
#from pynput.mouse import Controller
import ctypes, sys
from ctypes import wintypes, windll, WINFUNCTYPE, POINTER, c_int, c_void_p, c_long
from ctypes.wintypes import HHOOK, DWORD,WPARAM, LPARAM, MSG
import atexit
from threading import Thread
from queue import Queue
send_queue = Queue()
def send_worker():
    while True:
        try:
            encrypted = send_queue.get()
            sock.sendto(encrypted, (UDP_IP, UDP_PORT))
        except Exception as e:
            print(f"[SendWorker Error] {e}")

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
ctypes.windll.user32.ClipCursor(None)
ctypes.windll.user32.ShowCursor(False)
# Constants
WH_MOUSE_LL      =   14
WM_MOUSEMOVE     =   0x0200
WM_LBUTTONDOWN   =   0x0201
WM_LBUTTONUP     =   0x0202
WM_RBUTTONDOWN   =   0x0204
WM_RBUTTONUP     =   0x0205
WM_MOUSEWHEEL    =   0x020A
WM_MOUSEHWHEEL   =   0x020E
WHEEL_DELTA      =   120          # Windows standard
MAX_SCROLL_STEPS =   2            # cap per event (tweak this to 2 or 3 if too slow)
scroll_delta     =   0
# Screen Settings
screen_width  = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
center_x = screen_width // 2
center_y = screen_height // 2
# Mouse Re-Center Interval
RESET_INTERVAL = 0.5 # Seconds
WAIT_TIMEOUT = 100 # Mili Seconds
just_centered = False
last_reset = time.time()
reset_pending = False
EDGE_THRESHOLD = 30  # pixels from edge
VELOCITY_THRESHOLD = 50  # large jump triggers reset
RESET_COOLDOWN = 0.03  # ~30ms
reset_time = 0  # global variable
# 1) Define or alias LRESULT
wintypes.LRESULT = wintypes.LPARAM

key = "picoMouse"
UDP_IP = "192.168.1.102"  # Server IP
UDP_PORT = 443            # Server port

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

# Encrypt the data using key
def xor_crypt(data: bytes, key: str) -> bytes:
    key_bytes = key.encode("utf-8")
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])

def request_cursor_center():
    global reset_pending
    reset_pending = True

def perform_cursor_center():
    global reset_pending, last_reset
    if reset_pending and time.time() - last_reset > RESET_INTERVAL:
        user32.SetCursorPos(center_x, center_y)
        sleep(0.02)
        reset_pending = False
        last_reset = time.time()

def reset_deltas():
    global prev_x, prev_y
    x, y = user32.GetCursorPos()
    prev_x, prev_y = x, y

# Globals for tracking state
is_left_down=False
is_right_down=False
scroll_y = 0
scrol_x = 0
prev_x = None
prev_y = None
sock   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Thread(target=send_worker, daemon=True).start()
# — Hook prototypes
LRESULT = wintypes.LPARAM   # alias for a pointer‐sized signed int
LowLevelMouseProc = ctypes.WINFUNCTYPE(
    LRESULT,            # return type
    ctypes.c_int,       # nCode
    wintypes.WPARAM,    # wParam
    wintypes.LPARAM     # lParam
)

# — Structures
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.wintypes.LONG),
                ("y", ctypes.wintypes.LONG)]

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("pt", POINT),
        ("mouseData", ctypes.wintypes.DWORD),
        ("flags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))
    ]
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    class _INPUT_UNION(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]

    _anonymous_ = ("u",)
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("u", _INPUT_UNION)
    ]
user32.SetWindowsHookExW.argtypes = (ctypes.c_int, LowLevelMouseProc, wintypes.HINSTANCE, wintypes.DWORD)
user32.SetWindowsHookExW.restype  = wintypes.HHOOK
user32.CallNextHookEx.argtypes = (wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
user32.CallNextHookEx.restype  = LRESULT
user32.UnhookWindowsHookEx.argtypes = (wintypes.HHOOK,)
user32.UnhookWindowsHookEx.restype  = wintypes.BOOL
user32.GetMessageW.argtypes   = (ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT)
user32.GetMessageW.restype    = wintypes.BOOL
user32.TranslateMessage.argtypes  = (ctypes.POINTER(wintypes.MSG),)
user32.DispatchMessageW.argtypes = (ctypes.POINTER(wintypes.MSG),)


#@LowLevelMouseProc
def low_level_mouse_proc(nCode, wParam, lParam):
    global just_centered, is_left_down, is_right_down, scrol_x, scroll_y, scroll_delta, prev_x, prev_y, reset_time
    #print("[HOOK] Triggered")
    #ctypes.windll.user32.ShowCursor(False)
    if nCode != 0:
        return user32.CallNextHookEx(None, nCode, wParam, lParam)

    ms = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
    if ms.flags & 0x00000001:  # LLMHF_INJECTED
        return user32.CallNextHookEx(None, nCode, wParam, lParam)
    x, y = ms.pt.x, ms.pt.y
    

    
    #if just_centered:
    #    print("[HOOK] Reset Triggered")
        #user32.SetCursorPos(center_x, center_y)
        #pt = POINT()
        #ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        #x, y = pt.x, pt.y
    #    prev_x, prev_y = center_x, center_y
    #    just_centered= False
        #sleep(0.01)
    #    return user32.CallNextHookEx(None, nCode, wParam, lParam)
    #print("[HOOK] x:",str(x)+" y:",str(y))
    # Update Scroll Wheel
    if wParam == WM_MOUSEWHEEL:
        scroll_y= ctypes.c_short(ms.mouseData >>16).value
        raw = scroll_y
        scroll_delta = max(-MAX_SCROLL_STEPS, min(MAX_SCROLL_STEPS, raw))
    else: scroll_delta = 0
    #elif wParam == WM_MOUSEHWHEEL:
    #    scroll_x=ctypes.c_short(ms.mouseData >>16).value
    # Update Left button state
    if   wParam == WM_LBUTTONDOWN: is_left_down  = True
    elif wParam == WM_LBUTTONUP  : is_left_down  = False
    # Update Right button state
    if   wParam == WM_RBUTTONDOWN: is_right_down = True
    elif wParam == WM_RBUTTONUP  : is_right_down = False
    # Compute movement delta on every event
    if prev_x is not None:
        dx = x - prev_x
        dy = y - prev_y
    else:
        dx = dy = 0
    prev_x, prev_y = x, y
    print("[SENT] dx:",str(dx)+" dy:",str(dy))

    at_edge = (
        x <= EDGE_THRESHOLD or x >= screen_width - EDGE_THRESHOLD or
        y <= EDGE_THRESHOLD or y >= screen_height - EDGE_THRESHOLD
    )
    if at_edge:
        user32.BlockInput(True)
        #user32.SetCursorPos(center_x, center_y)
        
        input_struct = INPUT()
        input_struct.type = INPUT_MOUSE
        input_struct.mi = MOUSEINPUT()
        input_struct.mi.dx = center_x
        input_struct.mi.dy = center_y
        input_struct.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
        user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))

        
        time.sleep(0.01)
        user32.BlockInput(False)
        reset_time = time.time()
        just_centered = True
        prev_x, prev_y = center_x, center_y
        return user32.CallNextHookEx(None, nCode, wParam, lParam)

    now = time.time()
    if now - reset_time < RESET_COOLDOWN:
        # Skip processing until cursor settles
        return user32.CallNextHookEx(None, nCode, wParam, lParam)
    # send a long enough hold-duration (e.g. 200 ms) on every event while dragging
    left_click_duration=200 if is_left_down else 0
    right_flag = 1 if is_right_down else 0
    payload = f"{dx},{dy},{scroll_delta},{right_flag},0,{left_click_duration}".encode()

    encrypted  = xor_crypt(payload, key)
    try:
        send_queue.put(encrypted, block=False)
    except:
        pass
    return user32.CallNextHookEx(None, nCode, wParam, lParam)
# Wrap your function Globally
mouse_proc = LowLevelMouseProc(low_level_mouse_proc)
def install_hook():

    #hInstance = kernel32.GetModuleHandleW(None)

    # Then install the hook using the wrapped function
    hook = windll.user32.SetWindowsHookExW(WH_MOUSE_LL, mouse_proc, None, 0)
    if not hook:
        raise ctypes.WinError(ctypes.get_last_error())
    print(f"Hook installed (id={hook})")
    return hook

def uninstall_hook(hook):
    if hook:
        user32.UnhookWindowsHookEx(hook)
        print(f"Hook {hook} removed")
def hook_proc(nCode, wParam, lParam):
    if nCode == 0 and wParam == WM_MOUSEMOVE:
        ms = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
        x, y = ms.pt.x, ms.pt.y
        # Your delta logic here
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

if __name__ == "__main__":
    # must run as Administrator
    hook_id = install_hook()
    atexit.register(uninstall_hook, hook_id)
    # message loop to keep hook alive
    QS_ALLINPUT = 0x04FF
    INFINITE    = 0xFFFFFFFF
    PM_REMOVE = 0x0001
    msg = wintypes.MSG()
    try:
        while True:
            # Wait until there's any input (keyboard, mouse, posted, etc.)
            user32.MsgWaitForMultipleObjects(0, None, False, WAIT_TIMEOUT, QS_ALLINPUT)
            # pump Windows messages
            while user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, PM_REMOVE):
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
                
            #if time.time() - last_reset > RESET_INTERVAL:
            #    user32.SetCursorPos(center_x, center_y)
            #    #prev_x, prev_y = center_x, center_y
            #    last_reset = time.time()
            #    just_centered = True
                #sleep(0.005)
            # small pause
            sleep(0.005) # 0.005
    except KeyboardInterrupt:
        pass
    finally:
        user32.UnhookWindowsHookEx(hook_id)

# Mouse Movement i want to Flick
#       dx,dy,scroll,(left click duration 500 ms 0.5 second),(Right click press 1 enable, 0 disable)
# Order: dx,   dy, scroll, right_click, soft_reset, left_click_duration
#data =   "500,0,0,0,0,0"
#send(data)
