from ctypes import *

XEDPARSE_MAXBUFSIZE = 256
XEDPARSE_MAXASMSIZE = 16

XEDPARSE_ERROR = 0
XEDPARSE_OK = 1

class XEDPARSE(Structure):
    _pack_= 8
    _fields_ = [("x64", c_bool),
                ("cip", c_ulonglong),
                ("dest_size", c_uint),
                ("cbUnknown", c_void_p),
                ("dest", c_char * XEDPARSE_MAXASMSIZE),
                ("instr", c_char * XEDPARSE_MAXBUFSIZE),
                ("error", c_char * XEDPARSE_MAXBUFSIZE)
    ]

__module = CDLL('./libs/XEDParse.dll')
    
XEDParseAssemble = __module.XEDParseAssemble

def get_simple_asm_code(asm):
    parse = XEDPARSE()
    parse.x64 = 0
    parse.cip = 0
    parse.instr = asm.encode()
    result = XEDParseAssemble(byref(parse))
    if result:
        return parse.dest + (parse.dest_size - len(parse.dest)) * b'\x00'

def get_asm_code(asm):
    codes = b""
    code_list = []
    for i in asm.split("\n"):
        if i != "":
            codes += get_simple_asm_code(i)
    for i in codes:
        code_list.append(i)
    return code_list

def asm_format(asm):
    code = ""
    for i in asm:
        code += hex(i)[2:].rjust(2, "0")
    return code
