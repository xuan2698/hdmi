def reference(vectors):
    hh, mm, ss, pm = 0x12, 0x00, 0x00, 0
    out = []
    for v in vectors:
        reset = v.get('reset', 0)
        ena = v.get('ena', 0)

        if reset:
            hh, mm, ss, pm = 0x12, 0x00, 0x00, 0
        elif ena:
            ss += 1
            if (ss & 0x0F) == 0x0A:
                ss += 0x06
            if ss >= 0x60:
                ss = 0x00
                mm += 1
                if (mm & 0x0F) == 0x0A:
                    mm += 0x06
                if mm >= 0x60:
                    mm = 0x00
                    if hh == 0x12:
                        hh = 0x01
                    else:
                        if hh == 0x11:
                            pm ^= 1
                        hh += 1
                        if (hh & 0x0F) == 0x0A:
                            hh += 0x06

        out.append({'pm': pm, 'hh': hh, 'mm': mm, 'ss': ss})
    return out
