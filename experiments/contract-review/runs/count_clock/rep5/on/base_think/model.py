def reference(vectors):
    def inc(v):
        v += 1
        return v + 6 if (v & 15) > 9 else v
    reset = 0
    ena = 0
    hh = 0x12
    mm = 0
    ss = 0
    pm = 0
    out = []
    for row in vectors:
        for k in ('reset', 'ena'):
            if k in row:
                if k == 'reset':
                    reset = row[k]
                else:
                    ena = row[k]
        if reset:
            hh = 0x12
            mm = 0
            ss = 0
            pm = 0
        elif ena:
            if ss == 0x59:
                ss = 0
                if mm == 0x59:
                    mm = 0
                    if hh == 0x12:
                        hh = 0x01
                    elif hh == 0x11:
                        hh = 0x12
                        pm ^= 1
                    else:
                        hh = inc(hh)
                else:
                    mm = inc(mm)
            else:
                ss = inc(ss)
        out.append({'pm': pm, 'hh': hh, 'mm': mm, 'ss': ss})
        mid = row.get('mid')
        if mid:
            for k in ('reset', 'ena'):
                if k in mid:
                    if k == 'reset':
                        reset = mid[k]
                    else:
                        ena = mid[k]
    return out
