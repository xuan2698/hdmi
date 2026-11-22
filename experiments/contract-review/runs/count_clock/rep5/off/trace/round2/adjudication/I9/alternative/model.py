def reference(vectors):
    # Contract rules implemented:
    # R1_reset: synchronous active-high reset -> 12:00 AM (pm=0, hh=0x12, mm=0, ss=0)
    # R2_seconds: increment ss when ena and ss != 0x59
    # R3_seconds_rollover: ss 0x59 -> 0x00, mm increments (when mm != 0x59)
    # R4_minutes_rollover: mm 0x59 -> 0x00, hh increments; if hh==0x12 -> hh=0x01, pm unchanged
    # R5_hour_rollover_am_pm: hh 0x11 -> 0x12 and toggle pm
    # R6_hold: when ena==0 and reset==0, hold all state
    # hh is BCD 12-hour: 0x12 = 12 o'clock, 0x01 = 1 o'clock

    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # Initialize to reset value 12:00 AM
    ss = 0x00
    mm = 0x00
    hh = 0x12
    pm = 0

    results = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Compute next state (posedge behavior)
        if reset == 1:
            # R1_reset
            n_ss = 0x00
            n_mm = 0x00
            n_hh = 0x12
            n_pm = 0
        elif ena == 1:
            n_ss = ss
            n_mm = mm
            n_hh = hh
            n_pm = pm

            if ss != 0x59:
                # R2_seconds
                ss_ones = ss & 0x0F
                ss_tens = (ss >> 4) & 0x0F
                if ss_ones == 9:
                    ss_ones = 0
                    ss_tens += 1
                else:
                    ss_ones += 1
                n_ss = (ss_tens << 4) | ss_ones
            else:
                # R3_seconds_rollover
                n_ss = 0x00
                if mm != 0x59:
                    mm_ones = mm & 0x0F
                    mm_tens = (mm >> 4) & 0x0F
                    if mm_ones == 9:
                        mm_ones = 0
                        mm_tens += 1
                    else:
                        mm_ones += 1
                    n_mm = (mm_tens << 4) | mm_ones
                else:
                    # R4_minutes_rollover
                    n_mm = 0x00
                    if hh == 0x12:
                        # 12 -> 1, pm unchanged
                        n_hh = 0x01
                    elif hh == 0x11:
                        # R5_hour_rollover_am_pm: 11 -> 12, toggle pm
                        n_hh = 0x12
                        n_pm = 1 - pm
                    else:
                        hh_ones = hh & 0x0F
                        hh_tens = (hh >> 4) & 0x0F
                        if hh_ones == 9:
                            hh_ones = 0
                            hh_tens += 1
                        else:
                            hh_ones += 1
                        n_hh = (hh_tens << 4) | hh_ones
        else:
            # R6_hold
            n_ss = ss
            n_mm = mm
            n_hh = hh
            n_pm = pm

        # Apply next state (visible next cycle)
        ss = n_ss
        mm = n_mm
        hh = n_hh
        pm = n_pm

        results.append({
            'pm': pm & 0x1,
            'hh': hh & 0xFF,
            'mm': mm & 0xFF,
            'ss': ss & 0xFF,
        })

    return results
