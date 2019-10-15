# python-code-inject
Simple tool for code inject made by Python
## demo
```
from code_inject import get_info, asm_to_buf, create_memory

asm = """
pushad
push -1
push 02
mov eax, 2
push 5
mov ebx, dword ds:[0x755e0c]
mov ebx, dword ptr ds:[ebx+0x868]
push ebx
mov edx, 0x418d70
call edx
popad
ret 4
"""


get_info("Plants vs. Zombies")
buf = asm_to_buf(asm)
create_memory(buf)
```

## ref
> https://github.com/x64dbg/XEDParse
