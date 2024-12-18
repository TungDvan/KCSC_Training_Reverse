SBOX = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

def transpose4x4(m):
    return m[0::4] + m[1::4] + m[2::4] + m[3::4]

def list2hex(list):
    list = list[::-1]
    hex = ""
    for e in list:
        hex += "{:02X}".format(e)
    return hex

def hex2list(hex):
    byte_list = [hex[i:i+2] for i in range(0, len(hex), 2)][::-1]
    hex = ''.join(byte_list)
    lst = []
    if len(hex) % 2 == 0:
        for i in range(len(hex)//2):
            lst.append(int(hex[i*2:i*2+2], 16))
    return lst

def xor(bytelist1, bytelist2):
    res = []
    length = min(len(bytelist1), len(bytelist2))
    for i in range(length):
        res.append(bytelist1[i] ^ bytelist2[i])
    return res

def aesenc_cal(state, roundkey, last=False):
    def shift_rows(state):
        state[4], state[5], state[6], state[7] = state[5], state[6], state[7], state[4]
        state[8], state[9], state[10], state[11] = state[10], state[11], state[8], state[9]
        state[12], state[13], state[14], state[15] = state[15], state[12], state[13], state[14]

    def sub_bytes(state):
        for i in range(16):
            state[i] = SBOX[state[i]]

    def mix_columns(state):
        xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

        def mix_column(col):
            t = col[0] ^ col[1] ^ col[2] ^ col[3]
            u = col[0]
            col[0] ^= t ^ xtime(col[0] ^ col[1])
            col[1] ^= t ^ xtime(col[1] ^ col[2])
            col[2] ^= t ^ xtime(col[2] ^ col[3])
            col[3] ^= t ^ xtime(col[3] ^ u)
            return col

        out = [None]*16
        for i in range(0,4):
            out[i::4] = mix_column(state[i::4])
        return out

    sub_bytes(state)
    shift_rows(state)
    if not last:
        state = mix_columns(state)
    return xor(state, roundkey)

def aesenc(dat, k):
    data = transpose4x4(hex2list(dat.hex()))
    key = transpose4x4(hex2list(k.hex()))    
    res = transpose4x4(aesenc_cal(data, key))
    return bytes.fromhex(list2hex(res))

def aesenclast(dat, k):
    data = transpose4x4(hex2list(dat.hex()))
    key = transpose4x4(hex2list(k.hex()))    
    res = transpose4x4(aesenc_cal(data, key, last=True))
    return bytes.fromhex(list2hex(res))

map = [
    0xFF, 0xFE, 0xFD, 0xFC, 0xFB, 0xFA, 0xF9, 0xF8, 0xF7, 0xF6, 0xF5, 0xF4, 0xF3, 0xF2, 0xF1, 0xF0,
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F,
    0xB7, 0x73, 0xC2, 0x9F, 0xB3, 0x76, 0xC4, 0x98, 0xBB, 0x7F, 0xCE, 0x93, 0xB7, 0x72, 0xC0, 0x9C,
    0xB9, 0x51, 0xA8, 0xCD, 0xAD, 0x44, 0xBE, 0xDA, 0xB5, 0x5D, 0xA4, 0xC1, 0xA9, 0x40, 0xBA, 0xDE,
    0x8D, 0x87, 0xDF, 0x4C, 0x3E, 0xF1, 0x1B, 0xD4, 0x85, 0x8E, 0xD5, 0x47, 0x32, 0xFC, 0x15, 0xDB,
    0x9A, 0xE1, 0xF1, 0x74, 0x37, 0xA5, 0x4F, 0xAE, 0x82, 0xF8, 0xEB, 0x6F, 0x2B, 0xB8, 0x51, 0xB1,
    0xD6, 0x56, 0x17, 0xBD, 0xE8, 0xA7, 0x0C, 0x69, 0x6D, 0x29, 0xD9, 0x2E, 0x5F, 0xD5, 0xCC, 0xF5,
    0x55, 0xE2, 0xBA, 0x92, 0x62, 0x47, 0xF5, 0x3C, 0xE0, 0xBF, 0x1E, 0x53, 0xCB, 0x07, 0x4F, 0xE2,
    0xA9, 0xD2, 0x8F, 0xA2, 0x41, 0x75, 0x83, 0xCB, 0x2C, 0x5C, 0x5A, 0xE5, 0x73, 0x89, 0x96, 0x10,
    0xDA, 0x45, 0x2A, 0x58, 0xB8, 0x02, 0xDF, 0x64, 0x58, 0xBD, 0xC1, 0x37, 0x93, 0xBA, 0x8E, 0xD5,
    0x87, 0xCB, 0x8C, 0x7E, 0xC6, 0xBE, 0x0F, 0xB5, 0xEA, 0xE2, 0x55, 0x50, 0x99, 0x6B, 0xC3, 0x40,
    0x34, 0x3A, 0x04, 0x51, 0x8C, 0x38, 0xDB, 0x35, 0xD4, 0x85, 0x1A, 0x02, 0x47, 0x3F, 0x94, 0xD7,
    0xA7, 0xE9, 0x82, 0xDE, 0x61, 0x57, 0x8D, 0x6B, 0x8B, 0xB5, 0xD8, 0x3B, 0x12, 0xDE, 0x1B, 0x7B,
    0xFD, 0x27, 0xAB, 0x70, 0x71, 0x1F, 0x70, 0x45, 0xA5, 0x9A, 0x6A, 0x47, 0xE2, 0xA5, 0xFE, 0x90,
    0xC7, 0x52, 0xE2, 0x46, 0xA6, 0x05, 0x6F, 0x2D, 0x2D, 0xB0, 0xB7, 0x16, 0x3F, 0x6E, 0xAC, 0x6D
]

flag = [
    0x4b, 0x43, 0x53, 0x43, 0x7b, 0x53, 0x65, 0x72, 0x61, 0x64, 0x69, 0x70, 0x69, 0x74, 0x79, 0x4c,
    0x6f, 0x76, 0x65, 0x42, 0x48, 0x50, 0x53, 0x65, 0x72, 0x61, 0x64, 0x69, 0x70, 0x69, 0x74, 0x79,
    0x4c, 0x6f, 0x76, 0x65, 0x42, 0x48, 0x50, 0x53, 0x65, 0x72, 0x61, 0x64, 0x69, 0x70, 0x69, 0x74,
    0x79, 0x4c, 0x6f, 0x76, 0x65, 0x42, 0x48, 0x50, 0x53, 0x65, 0x72, 0x61, 0x64, 0x69, 0x70, 0x69,
    0x74, 0x79, 0x4c, 0x6f, 0x76, 0x65, 0x42, 0x48, 0x50, 0x53, 0x65, 0x72, 0x61, 0x64, 0x69, 0x70,
    0x69, 0x74, 0x79, 0x4c, 0x6f, 0x76, 0x65, 0x42, 0x48, 0x50, 0x53, 0x65, 0x72, 0x61, 0x64, 0x69,
    0x70, 0x69, 0x74, 0x79, 0x4c, 0x6f, 0x76, 0x65, 0x42, 0x48, 0x50, 0x53, 0x65, 0x72, 0x61, 0x64,
    0x69, 0x70, 0x69, 0x74, 0x79, 0x4c, 0x6f, 0x76, 0x65, 0x42, 0x48, 0x50, 0x53, 0x65, 0x72, 0x61,
    0x64, 0x69, 0x70, 0x69, 0x74, 0x79, 0x4c, 0x6f, 0x76, 0x65, 0x42, 0x48, 0x50, 0x53, 0x7d, 0x0A
]

is_0x10 = [
    0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10
]

def _xor(a, b):
    map = []
    for i in range(len(a)):
        map.append(a[i] ^ b[i])
    return map

def _print_xmm(a):
    a = list(a[::-1])
    for i in range(len(a)): print(end = f'0x{a[i]:02X}, ')
    print()

if __name__ == "__main__":
    ans = []
    for i in range(0, len(flag) + 0x10, 0x10):
        if i == len(flag): v12 = is_0x10[::]
        else: v12 = flag[i:i+0x10]
        vars0 = map[0:0x10]
        vars10 = map[0x10:0x20]
        _XMM0 = _xor(_xor(v12, vars0), vars10)
        _XMM1 = map[0x20:0x30]
        _XMM2 = map[0x30:0x40]
        _XMM3 = map[0x40:0x50]
        _XMM4 = map[0x50:0x60]
        _XMM5 = map[0x60:0x70]
        _XMM6 = map[0x70:0x80]
        _XMM7 = map[0x80:0x90]
        _XMM0 = bytes(_XMM0[::-1])
        _XMM1 = bytes(_XMM1[::-1])
        _XMM2 = bytes(_XMM2[::-1])
        _XMM3 = bytes(_XMM3[::-1])
        _XMM4 = bytes(_XMM4[::-1])
        _XMM5 = bytes(_XMM5[::-1])
        _XMM6 = bytes(_XMM6[::-1])
        _XMM7 = bytes(_XMM7[::-1])
        _XMM0 = aesenc(_XMM0, _XMM1)
        _XMM0 = aesenc(_XMM0, _XMM2)
        _XMM0 = aesenc(_XMM0, _XMM3)
        _XMM0 = aesenc(_XMM0, _XMM4)
        _XMM0 = aesenc(_XMM0, _XMM5)
        _XMM0 = aesenc(_XMM0, _XMM6)
        _XMM0 = aesenc(_XMM0, _XMM7)
        _XMM1 = map[0x90:0xA0]
        _XMM2 = map[0xA0:0xB0]
        _XMM3 = map[0xB0:0xC0]
        _XMM4 = map[0xC0:0xD0]
        _XMM5 = map[0xD0:0xE0]
        _XMM6 = map[0xE0:0xF0]
        _XMM7 = map[0xF0:0x100]
        _XMM1 = bytes(_XMM1[::-1])
        _XMM2 = bytes(_XMM2[::-1])
        _XMM3 = bytes(_XMM3[::-1])
        _XMM4 = bytes(_XMM4[::-1])    
        _XMM5 = bytes(_XMM5[::-1])
        _XMM6 = bytes(_XMM6[::-1])
        _XMM7 = bytes(_XMM7[::-1])
        _XMM0 = aesenc(_XMM0, _XMM1)
        _XMM0 = aesenc(_XMM0, _XMM2)
        _XMM0 = aesenc(_XMM0, _XMM3)
        _XMM0 = aesenc(_XMM0, _XMM4)
        _XMM0 = aesenc(_XMM0, _XMM5)
        _XMM0 = aesenc(_XMM0, _XMM6)
        _XMM0 = aesenclast(_XMM0, _XMM7)
        _XMM0 = list(_XMM0)
        _XMM0 = _XMM0[::-1]
        ans += _XMM0
        map[0:0x10] = _XMM0
    for i in range(len(ans)):
        if i % 16 == 15: print(f'0x{ans[i]:02X}', end = ',\n')
        else: print(f'0x{ans[i]:02X}', end = ', ')