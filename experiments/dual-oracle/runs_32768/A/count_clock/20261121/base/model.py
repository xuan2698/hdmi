def reference(vectors):
    hh, mm, ss, pm = 12, 0, 0, 0
    inputs = {'reset': 0, 'ena': 0}
    out = []
    for row in vectors:
        for k in row:
            if k != 'mid':
                inputs[k] = row[k]
        if inputs.get('reset', 0):
            hh, mm, ss, pm = 12, 0, 0, 0
        elif inputs.get('ena', 0):
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
        hh_bcd = ((hh // 10) << 4) | (hh % 10)
        mm_bcd = ((mm // 10) << 4) | (mm % 10)
        ss_bcd = ((ss // 10) << 4) | (ss % 10)
        out.append({'pm': pm, 'hh': hh_bcd, 'mm': mm_bcd, 'ss': ss_bcd})
        if 'mid' in row:
            for k, v in row['mid'].items():
                inputs[k] = v
    return out
