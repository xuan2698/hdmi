def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # hh is BCD 12-hour: 0x12 = 12 o'clock, 0x01 = 1 o'clock, etc.
    # Reset value: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
    ss_ones = 0
    ss_tens = 0
    mm_ones = 0
    mm_tens = 0
    hh_ones = 2
    hh_tens = 1
    pm_state = 0

    results = []
    for vec in vectors:
        reset = vec.get('reset', 0)
        ena = vec.get('ena', 0)

        # Compute outputs for this row (current state, before edge)
        hh = (hh_tens << 4) | hh_ones
        mm = (mm_tens << 4) | mm_ones
        ss = (ss_tens << 4) | ss_ones
        results.append({'pm': pm_state, 'hh': hh, 'mm': mm, 'ss': ss})

        # R1_reset: reset has priority, synchronous, resets to 12:00 AM
        if reset == 1:
            ss_ones = 0
            ss_tens = 0
            mm_ones = 0
            mm_tens = 0
            hh_ones = 2
            hh_tens = 1
            pm_state = 0
            continue

        # R6_hold: no enable, hold state
        if ena == 0:
            continue

        # ena == 1, reset == 0: increment
        # R2_seconds: increment seconds if not at 59
        if ss != 0x59:
            if ss_ones == 9:
                ss_ones = 0
                ss_tens += 1
            else:
                ss_ones += 1
            continue

        # ss == 0x59: seconds rollover
        ss_ones = 0
        ss_tens = 0

        # R3_seconds_rollover: increment minutes if not at 59
        if mm != 0x59:
            if mm_ones == 9:
                mm_ones = 0
                mm_tens += 1
            else:
                mm_ones += 1
            continue

        # mm == 0x59: minutes rollover
        mm_ones = 0
        mm_tens = 0

        # R4_minutes_rollover: increment hours if not at 12 (0x12)
        if hh != 0x12:
            # hh is BCD 12-hour: 0x01..0x09, 0x10, 0x11, 0x12
            if hh_ones == 9:
                hh_ones = 0
                hh_tens += 1
            else:
                hh_ones += 1
            continue

        # R5_hour_rollover_am_pm: hh == 0x12 (12 o'clock), roll to 1, toggle pm
        hh_ones = 1
        hh_tens = 0
        pm_state = 1 - pm_state

    return results
