def reference(vectors):
    hh = 0x12
    mm = 0
    ss = 0
    pm = 0
    out = []
    for r in vectors:
        if r.get("reset", 0):
            hh = 0x12
            mm = 0
            ss = 0
            pm = 0
        elif r.get("ena", 0):
            if ss == 0x59:
                ss = 0
                if mm == 0x59:
                    mm = 0
                    if hh == 0x11:
                        hh = 0x12
                        pm = 1 - pm
                    elif hh == 0x12:
                        hh = 0x01
                    else:
                        lo = hh & 0x0f
                        if lo == 9:
                            hh = ((hh >> 4) + 1) << 4
                        else:
                            hh = (hh & 0xf0) | (lo + 1)
                else:
                    lo = mm & 0x0f
                    if lo == 9:
                        mm = ((mm >> 4) + 1) << 4
                    else:
                        mm = (mm & 0xf0) | (lo + 1)
            else:
                lo = ss & 0x0f
                if lo == 9:
                    ss = ((ss >> 4) + 1) << 4
                else:
                    ss = (ss & 0xf0) | (lo + 1)
        out.append({"pm": pm, "hh": hh, "mm": mm, "ss": ss})
    return out
