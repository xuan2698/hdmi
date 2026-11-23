def reference(vectors):
    hh = 12
    mm = 0
    ss = 0
    pm = 0
    result = []
    for v in vectors:
        if isinstance(v, dict):
            reset = v.get('reset', 0)
            ena = v.get('ena', 0)
        else:
            reset = v[0] if len(v) > 0 else 0
            ena = v[1] if len(v) > 1 else 0
        if reset:
            hh = 12
            mm = 0
            ss = 0
            pm = 0
        elif ena:
            ss += 1
            if ss == 60:
                ss = 0
                mm += 1
                if mm == 60:
                    mm = 0
                    hh += 1
                    if hh == 13:
                        hh = 1
                    if hh == 12:
                        pm ^= 1
        hh_bcd = (hh // 10) * 16 + (hh % 10)
        mm_bcd = (mm // 10) * 16 + (mm % 10)
        ss_bcd = (ss // 10) * 16 + (ss % 10)
        result.append({'pm': pm, 'hh': hh_bcd, 'mm': mm_bcd, 'ss': ss_bcd})
    return result
