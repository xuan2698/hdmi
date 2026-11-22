def reference(vectors):
    # State representation: binary counts, converted to BCD for outputs.
    pm = 0
    hh = 12
    mm = 0
    ss = 0
    cur_reset = 0
    cur_ena = 0
    result = []
    for row in vectors:
        if 'reset' in row:
            cur_reset = row['reset']
        if 'ena' in row:
            cur_ena = row['ena']
        reset = cur_reset
        ena = cur_ena
        # Rule sync_reset_priority: synchronous reset has priority over ena.
        if reset == 1:
            pm = 0
            hh = 12
            mm = 0
            ss = 0
        # Rule normal_ena_increment: increment on ena when reset==0.
        elif ena == 1:
            ss += 1
            if ss == 60:
                ss = 0
                mm += 1
                if mm == 60:
                    mm = 0
                    if hh == 11:
                        hh = 12
                        if pm == 1:
                            pm = 0
                        else:
                            pm = 1
                    elif hh == 12:
                        hh = 1
                    else:
                        hh += 1
        # Rule hold_without_ena: otherwise hold (implicit).
        # Convert binary counts to BCD for outputs.
        ss_bcd = (ss // 10) * 16 + (ss % 10)
        mm_bcd = (mm // 10) * 16 + (mm % 10)
        hh_bcd = (hh // 10) * 16 + (hh % 10)
        d = {}
        d['pm'] = pm
        d['hh'] = hh_bcd
        d['mm'] = mm_bcd
        d['ss'] = ss_bcd
        result.append(d)
        # Optional mid input changes occur after sampling and carry to next row.
        if 'mid' in row and row['mid'] is not None:
            mid = row['mid']
            if 'reset' in mid:
                cur_reset = mid['reset']
            if 'ena' in mid:
                cur_ena = mid['ena']
    return result
