def reference(vectors):
    pm = 0
    hh = 0x12
    mm = 0
    ss = 0
    out = []
    for v in vectors:
        reset = v.get('reset', 0)
        ena = v.get('ena', 0)
        if reset:
            pm = 0
            hh = 0x12
            mm = 0
            ss = 0
        elif ena:
            if ss == 0x59:
                ss = 0
                if mm == 0x59:
                    mm = 0
                    if hh == 0x12:
                        hh = 0x01
                    elif hh == 0x11:
                        hh = 0x12
                        pm = 1 - pm
                    elif (hh & 0x0F) == 0x09:
                        hh = hh + 0x07
                    else:
                        hh = hh + 1
                else:
                    if (mm & 0x0F) == 0x09:
                        mm = mm + 0x07
                    else:
                        mm = mm + 1
            else:
                if (ss & 0x0F) == 0x09:
                    ss = ss + 0x07
                else:
                    ss = ss + 1
        out.append({'pm': pm, 'hh': hh, 'mm': mm, 'ss': ss})
    return out