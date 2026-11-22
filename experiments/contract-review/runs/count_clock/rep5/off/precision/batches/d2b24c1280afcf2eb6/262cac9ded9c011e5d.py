def reference(vectors):
    ss_ones, ss_tens = 0, 0
    mm_ones, mm_tens = 0, 0
    hh_ones, hh_tens = 2, 1  # 0x12 = 12
    pm_state = 0
    out = []
    for v in vectors:
        reset = v['reset']
        ena = v['ena']
        ss = (ss_tens << 4) | ss_ones
        mm = (mm_tens << 4) | mm_ones
        hh = (hh_tens << 4) | hh_ones
        out.append({'pm': pm_state, 'hh': hh, 'mm': mm, 'ss': ss})
        if reset:
            ss_ones, ss_tens = 0, 0
            mm_ones, mm_tens = 0, 0
            hh_ones, hh_tens = 2, 1
            pm_state = 0
        elif ena:
            if ss != 0x59:
                if ss_ones == 9:
                    ss_ones = 0
                    ss_tens += 1
                else:
                    ss_ones += 1
            else:
                ss_ones, ss_tens = 0, 0
                if mm != 0x59:
                    if mm_ones == 9:
                        mm_ones = 0
                        mm_tens += 1
                    else:
                        mm_ones += 1
                else:
                    mm_ones, mm_tens = 0, 0
                    if hh != 0x12:
                        if hh == 0x09:
                            hh_ones, hh_tens = 0, 1
                        elif hh == 0x11:
                            hh_ones, hh_tens = 2, 1
                        else:
                            hh_ones += 1
                    else:
                        hh_ones, hh_tens = 1, 0
                        pm_state = 1 - pm_state
    return out