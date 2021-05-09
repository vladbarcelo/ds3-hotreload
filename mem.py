import win32api
import win32process
from ReadWriteMemory import ReadWriteMemory
import ctypes
import time

MEM_COMMIT = 0x00001000
MEM_RESERVE = 0x00002000
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_RELEASE = 0x00008000
MEM_DECOMMIT = 0x00004000
PAGE_EXECUTE_READWRITE = 0x40
EXECUTE_IMMEDIATELY = 0x00000000


class _SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [('nLength',  ctypes.wintypes.DWORD),
                ('lpSecurityDescriptor',  ctypes.wintypes.LPVOID),
                ('bInheritHandle',  ctypes.wintypes.BOOL), ]


SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES
LPSECURITY_ATTRIBUTES = ctypes.POINTER(_SECURITY_ATTRIBUTES)
LPTHREAD_START_ROUTINE = ctypes.wintypes.LPVOID


def readMem(process, addr):
    ptr = process.get_pointer(addr)
    read_buffer = ctypes.c_uint()
    lp_buffer = ctypes.byref(read_buffer)
    n_size = ctypes.sizeof(read_buffer)
    lp_number_of_bytes_read = ctypes.c_uint(0)
    ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
    ReadProcessMemory.argtypes = [
        ctypes.wintypes.HANDLE, ctypes.wintypes.LPCVOID, ctypes.wintypes.LPVOID, ctypes.c_size_t, ctypes.c_uint]

    ReadProcessMemory(process.handle, addr, lp_buffer,
                      n_size, lp_number_of_bytes_read)
    return process.read(ptr)


def readWithOffsets(process, bAddr, offsets):
    addrPointer = bAddr
    value = readMem(process, addrPointer)
    for offset in offsets:
        addrPointer = offset + 0x7ff400000000 + value
        value = readMem(process, addrPointer)

    return value


def writeMem(process, bAddr, buf):
    WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
    WriteProcessMemory.argtypes = [
        ctypes.wintypes.HANDLE, ctypes.wintypes.LPVOID, ctypes.wintypes.LPCVOID, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD]
    WriteProcessMemory(
        process.handle, bAddr, buf, len(buf), 0)


def writeWithOffsets(process, bAddr, offsets, buf):
    addrPointer = bAddr
    value = readMem(process, addrPointer)
    for offset in offsets:
        addrPointer = offset + 0x7ff400000000 + value
        value = readMem(process, addrPointer)
    print(f'Writing to addr: {hex(addrPointer)}')
    writeMem(process, addrPointer, buf)


def getProcess():
    rwm = ReadWriteMemory()
    process = rwm.get_process_by_name('DarkSoulsIII.exe')
    process.open()
    return process


def getBaseAddr(pid):
    processHandle = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    modules = win32process.EnumProcessModulesEx(processHandle, 0x02)
    base_addr = modules[0]
    processHandle.close()
    return base_addr


def alloc(process, addr, length):
    alloc_addr = None
    VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
    VirtualAllocEx.restype = ctypes.wintypes.LPVOID
    VirtualAllocEx.argtypes = [
        ctypes.wintypes.HANDLE, ctypes.wintypes.LPVOID, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD]
    alloc_addr = VirtualAllocEx(process.handle, addr, length, MEM_COMMIT |
                                MEM_RESERVE, PAGE_EXECUTE_READWRITE)
    print(hex(addr), alloc_addr)
    while alloc_addr == None:
        addr += 0x000010000
        alloc_addr = VirtualAllocEx(process.handle, addr, length, MEM_COMMIT |
                                    MEM_RESERVE, PAGE_EXECUTE_READWRITE)
        print(hex(addr), alloc_addr)
        time.sleep(1)
    return alloc_addr


def free(process, addr):
    VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
    VirtualFreeEx.argtypes = [
        ctypes.wintypes.HANDLE, ctypes.wintypes.LPVOID, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD]
    VirtualFreeEx(process.handle, addr, 0, MEM_RELEASE)


def create_thread(hProcess, lpStartAddress, dwStackSize=0, lpParameter=0, dwCreationFlags=EXECUTE_IMMEDIATELY, lpThreadId=0, lpSecurityDescriptor=0, bInheritHandle=False):
    CreateRemoteThread = ctypes.windll.kernel32.CreateRemoteThread
    CreateRemoteThread.restype = ctypes.wintypes.HANDLE
    CreateRemoteThread.argtypes = (
        ctypes.wintypes.HANDLE, LPSECURITY_ATTRIBUTES, ctypes.wintypes.DWORD, LPTHREAD_START_ROUTINE, ctypes.wintypes.LPVOID, ctypes.wintypes.DWORD, ctypes.wintypes.LPDWORD)
    ThreadAttributes = SECURITY_ATTRIBUTES(ctypes.sizeof(
        SECURITY_ATTRIBUTES), lpSecurityDescriptor, bInheritHandle)
    lpThreadAttributes = LPSECURITY_ATTRIBUTES(ThreadAttributes)
    handle = CreateRemoteThread(hProcess, lpThreadAttributes, dwStackSize,
                                lpStartAddress, lpParameter, dwCreationFlags, lpThreadId)

    if handle is None or handle == 0:
        raise Exception('Error: %s' % GetLastError())

    return handle


def createThreadSimple(process, addr):
    thread_id = ctypes.wintypes.DWORD()

    create_thread(process.handle, addr,
                  lpThreadId=ctypes.wintypes.LPDWORD(thread_id))
