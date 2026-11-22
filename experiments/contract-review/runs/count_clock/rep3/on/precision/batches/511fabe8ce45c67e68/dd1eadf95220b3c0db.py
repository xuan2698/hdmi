def reference(vectors):
    pm = 0
    hh = 0x12
    mm = 0x00
    ss = 0x00
    out = []
    def inc_bcd(x):
        lo = x & 0x0F
        hi = (x >> 4) & 0x0F
        lo += 1
        if lo == 10:
            lo = 0
            hi += 1
        return ((hi & 0x0F) << 4) | (lo & 0x0F)
    for v in vectors:
        reset = v.get('reset', 0)
        ena = v.get('ena', 0)
        if reset:
            pm = 0
            hh = 0x12
            mm = 0x00
            ss = 0x00
        elif ena:
            carry = False
            if ss == 0x59:
                ss = 0x00
                carry = True
            else:
                ss = inc_bcd(ss)
            if carry:
                if mm == 0x59:
                    mm = 0x00
                    carry = True
                else:
                    mm = inc_bcd(mm)
                    carry = False
                if carry:
                    if hh == 0x11:
                        hh = 0x12
                        pm = 1 - pm
                    elif hh == 0x12:
                        hh = 0x01
                    else:
                        hh = inc_bcd(hh)
        out.append({'pm': pm & 1, 'hh': hh & 0xFF, 'mm': mm & 0xFF, 'ss': ss & 0xFF})
    return out