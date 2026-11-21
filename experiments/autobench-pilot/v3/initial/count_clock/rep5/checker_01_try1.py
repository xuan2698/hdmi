def reference(vectors):
    st = {'hh': 0x12, 'mm': 0, 'ss': 0, 'pm': 0}
    out = []
    for row in vectors:
        if row.get('reset', 0):
            st = {'hh': 0x12, 'mm': 0, 'ss': 0, 'pm': 0}
        elif row.get('ena', 0):
            ss = st['ss'] + 1
            mm = st['mm']
            hh = st['hh']
            pm = st['pm']
            if ss == 0x60:
                ss = 0
                mm += 1
                if mm == 0x60:
                    mm = 0
                    hh += 1
                    if hh == 0x13:
                        hh = 0x01
                        pm ^= 1
                    elif hh == 0x10:
                        hh = 0x10
                    elif hh & 0x0F == 0x0A:
                        hh = (hh & 0xF0) + 0x10
            st = {'hh': hh, 'mm': mm, 'ss': ss, 'pm': pm}
        out.append({'pm': st['pm'], 'hh': st['hh'], 'mm': st['mm'], 'ss': st['ss']})
        if 'mid' in row:
            m = row['mid']
            if 'reset' in m and m['reset']:
                st = {'hh': 0x12, 'mm': 0, 'ss': 0, 'pm': 0}
            elif 'ena' in m and m['ena']:
                ss = st['ss'] + 1
                mm = st['mm']
                hh = st['hh']
                pm = st['pm']
                if ss == 0x60:
                    ss = 0
                    mm += 1
                    if mm == 0x60:
                        mm = 0
                        hh += 1
                        if hh == 0x13:
                            hh = 0x01
                            pm ^= 1
                        elif hh & 0x0F == 0x0A:
                            hh = (hh & 0xF0) + 0x10
                st = {'hh': hh, 'mm': mm, 'ss': ss, 'pm': pm}
    return out
