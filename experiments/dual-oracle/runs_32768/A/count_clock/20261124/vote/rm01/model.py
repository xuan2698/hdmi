def reference(vectors):
    hh, mm, ss, pm = 0x12, 0, 0, 0

    def inc(x):
        return ((x >> 4) + 1) << 4 if (x & 15) == 9 else x + 1

    out = []
    for v in vectors:
        r = v['reset'] if isinstance(v, dict) else v[0]
        e = v['ena'] if isinstance(v, dict) else v[1]

        if r:
            hh, mm, ss, pm = 0x12, 0, 0, 0
        elif e:
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

    return out
