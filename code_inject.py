from ctypes import *
import win32api
import win32con
import win32gui
import win32process

from xed_parse import get_asm_code, get_simple_asm_code, asm_format

hwnd = None
h_process = None
k32 = CDLL("kernel32.dll")


def get_info(name):
    global hwnd
    global h_process
    hwnd = win32gui.FindWindow(None, name)
    if not hwnd:
        print("Find Window Failed! Please check the window name")
        return 
    hid, pid = win32process.GetWindowThreadProcessId(hwnd)
    if not hid:
        print("Get Thread Id Failed! Please check the window name")
        return 
    h_process = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    if not h_process:
        print("Open Process Failed! Please check the privilege")
        return


def asm_to_buf(asm):
    codes = get_asm_code(asm)
    length = len(codes)
    print("Byte Code: ", asm_format(codes))
    buf = create_string_buffer(length)
    buf.raw = bytearray(codes)
    return buf


def create_memory(buf):
    global h_process

    if not h_process:
        print("Open Process Failed! Please check the privilege")
        return    


    # Alloc memory and write
    code_block = create_string_buffer(len(buf))
    start_address = k32.VirtualAllocEx(int(h_process), None, len(buf), win32con.MEM_COMMIT, win32con.PAGE_EXECUTE_READWRITE)
    ret = k32.WriteProcessMemory(int(h_process), start_address, buf, len(buf), None)
    if not ret:
        print("Write MEmory Failed!")
        return
    
    # Create remote thread to execute
    thread_id = c_int()
    h_remote_thread = k32.CreateRemoteThread(int(h_process), None, 0, start_address, None, 0, byref(thread_id))
    if not h_remote_thread:
        print("Create Remote Thread Failed")
        return
    print("Thread id: ", thread_id.value)

    # close handle
    win32api.CloseHandle(h_remote_thread) 
    win32api.CloseHandle(h_process)
