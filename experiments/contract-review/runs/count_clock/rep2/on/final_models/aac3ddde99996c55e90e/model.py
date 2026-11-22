def reference(vectors):
    # Initial power-up choice: 12:00 AM (concrete, as required).
    pm = 0
    hh = 0x12
    mm = 0
    ss = 0

    # Current input values carried between sampled edges.
    cur = {'reset': 0, 'ena': 0, 'clk': 0}
    out = []

    def inc_bcd(v):
        lo = v & 0x0F
        hi = (v >> 4) & 0x0F
        lo += 1
        if lo == 10:
            lo = 0
            hi += 1
        # For 00-59 BCD counters: 0x5A => wrap to 0x00.
        if hi == 6:
            hi = 0
        return (hi << 4) | lo

    def inc_hour(h, p):
        # 11 -> 12 toggles AM/PM.
        if h == 0x11:
            return 0x12, p ^ 1
        # 12 -> 01 does not toggle AM/PM.
        if h == 0x12:
            return 0x01, p
        # 01-10 or 00 -> next BCD value.
        lo = h & 0x0F
        hi = (h >> 4) & 0x0F
        lo += 1
        if lo == 10:
            lo = 0
            hi += 1
        return (hi << 4) | lo, p

    def apply_mid(changes):
        if isinstance(changes, dict):
            for k, v in changes.items():
                if k in cur:
                    cur[k] = v
        elif isinstance(changes, list):
            for c in changes:
                apply_mid(c)

    for row in vectors:
        # Values driven before the sampled posedge.
        if 'reset' in row:
            cur['reset'] = row['reset']
        if 'ena' in row:
            cur['ena'] = row['ena']
        if 'clk' in row:
            cur['clk'] = row['clk']

        # R_RESET: synchronous reset has priority over enable.
        if cur['reset'] == 1:
            pm = 0
            hh = 0x12
            mm = 0
            ss = 0
        else:
            # R_NORMAL: increment when enabled, otherwise hold.
            if cur['ena'] == 1:
                ss_old = ss
                ss = inc_bcd(ss)
                if ss_old == 0x59:
                    mm_old = mm
                    mm = inc_bcd(mm)
                    if mm_old == 0x59:
                        hh, pm = inc_hour(hh, pm)

        out.append({
            'pm': pm & 1,
            'hh': hh & 0xFF,
            'mm': mm & 0xFF,
            'ss': ss & 0xFF
        })

        # Optional mid changes occur after sampling and carry to next row.
        if 'mid' in row:
            apply_mid(row['mid'])
        if 'mid_changes' in row:
            apply_mid(row['mid_changes'])
        if 'midcycle' in row:
            apply_mid(row['midcycle'])
        for k, v in row.items():
            if k.startswith('mid_') and k != 'mid_changes':
                name = k[4:]
                if name in cur:
                    cur[name] = v

    return out
