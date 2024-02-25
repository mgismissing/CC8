import sys, msvcrt as m

class dev:
    try:
        d = int(sys.argv[2])
    except ValueError:
        print(f"dev: cannot set value dev.d to \"{sys.argv[2]}\"")
        exit(-256)
    except IndexError:
        d = 0

class uint8:
    def convert(a: int):
        return a & 0xFF

class cc8:
    class reg:
        def convert(a: int):
            """Converts a register hexcode [a] to its variable"""
            if a == 0x00: return cc8.reg.ax
            if a == 0x01: return cc8.reg.bx
            if a == 0x02: return cc8.reg.cx
            if a == 0x03: return cc8.reg.dx
            if a == 0x04: return cc8.reg.f.zf
            if a == 0x05: return cc8.reg.f.gf
            if a == 0x06: return cc8.reg.f.lf
            if a == 0x07: return cc8.reg.f.pf
            if a == 0x08: return cc8.reg.f.cf
        def assign(a: int, b: int):
            """Sets the variable of a register hexcode [a] to a variable [b]"""
            if a == 0x00: cc8.reg.ax = b
            if a == 0x01: cc8.reg.bx = b
            if a == 0x02: cc8.reg.cx = b
            if a == 0x03: cc8.reg.dx = b
            if a == 0x04: exit("CANNOT MVV / MVR TO ZF")
            if a == 0x05: exit("CANNOT MVV / MVR TO GF")
            if a == 0x06: exit("CANNOT MVV / MVR TO LF")
            if a == 0x07: exit("CANNOT MVV / MVR TO PF")
            if a == 0x08: exit("CANNOT MVV / MVR TO CF")
        class f:
            zf = 0 # Zero [a = 0]
            gf = 0 # Greater Than Flag [a >> b]
            lf = 0 # Less Than Flag [a << b]
            pf = 0 # Parity Flag [a == b]
            cf = 0 # Carry Flag [int(str(a + b)[8]) >> 0]
        ax = 0 # General Purpose Register A
        bx = 0 # General Purpose Register B
        cx = 0 # General Purpose Register C
        dx = 0 # General Purpose Register D
    class idt:
        def int(code: int):
            if code == 0x01: # Screen operations
                if cc8.reg.ax == 0x01: # PRINT BX
                    print(end=chr(cc8.reg.bx), flush=True)
            if code == 0x02: # Input operations
                if cc8.reg.ax == 0x01: # GETCH BX
                    cc8.reg.bx = uint8.convert(ord(m.getch()))
class c:
    op = 0
    a = 0
    b = 0

try:
    with open(sys.argv[1], "rb") as bfile:
        file = [byte for byte in bfile.read()]
except IndexError:
    print(f"Missing input file.")
    exit(-1)
except FileNotFoundError:
    print(f"File \"{sys.argv[1]}\" doesn't exist.")
    exit(-2)

i = 0
while i <= len(file):
    try: c.op = file[i]
    except: c.op = 0
    try: c.a = file[i+1]
    except: c.a = 0
    try: c.b = file[i+2]
    except: c.b = 0
    
    if dev.d == 1:
        print(f"CURRENT OP {hex(c.op)}")
        print(f"CURRENT ARG A {hex(c.a)}")
        print(f"CURRENT ARG B {hex(c.b)}")

    if c.op == 0x00: #NOP
        i += 1
    elif c.op == 0x01: #MVV
        cc8.reg.assign(c.a, c.b)
        cc8.reg.assign(c.a, uint8.convert(cc8.reg.convert(c.a)))
        i += 3
    elif c.op == 0x02: #MVR
        cc8.reg.assign(c.a, cc8.reg.convert(c.b))
        cc8.reg.assign(c.a, uint8.convert(cc8.reg.convert(c.a)))
        i += 3
    elif c.op == 0x03: #INC
        cc8.reg.assign(c.a, cc8.reg.convert(c.a) + 1)
        cc8.reg.assign(c.a, uint8.convert(cc8.reg.convert(c.a)))
        i += 2
    elif c.op == 0x04: #DEC
        cc8.reg.assign(c.a, cc8.reg.convert(c.a) - 1)
        cc8.reg.assign(c.a, uint8.convert(cc8.reg.convert(c.a)))
        i += 2
    elif c.op == 0x05: #ADD
        cc8.reg.assign(c.a, cc8.reg.convert(c.a) + cc8.reg.convert(c.b))
        cc8.reg.assign(c.a, uint8.convert(cc8.reg.convert(c.a)))
        i += 3
    elif c.op == 0x06: #SUB
        cc8.reg.assign(c.a, cc8.reg.convert(c.a) - cc8.reg.convert(c.b))
        cc8.reg.assign(c.a, uint8.convert(cc8.reg.convert(c.a)))
        i += 3
    elif c.op == 0x07: #CMP
        cc8.reg.f.zf = cc8.reg.convert(c.a) == 0
        cc8.reg.f.gf = cc8.reg.convert(c.a) >> cc8.reg.convert(c.b)
        cc8.reg.f.lf = cc8.reg.convert(c.a) << cc8.reg.convert(c.b)
        cc8.reg.f.pf = cc8.reg.convert(c.a) == cc8.reg.convert(c.b)
        i += 3
    elif c.op == 0x08: #INT
        cc8.idt.int(c.a)
        i += 2
    elif c.op == 0x09: #JMP
        i = c.a * 256 + c.b
    else:
        print(f"INVALID OPCODE AT {hex(i)}")

    if dev.d == 1:
        print(f"AX {hex(cc8.reg.ax)}")
        print(f"BX {hex(cc8.reg.bx)}")
        print(f"CX {hex(cc8.reg.cx)}")
        print(f"DX {hex(cc8.reg.dx)}")
        print(f"ZF {hex(cc8.reg.f.zf)}")
        print(f"GF {hex(cc8.reg.f.gf)}")
        print(f"LF {hex(cc8.reg.f.lf)}")
        print(f"PF {hex(cc8.reg.f.pf)}")
        print(f"CF {hex(cc8.reg.f.cf)}")
        print("- - - - - - - - - - - - - - - -")