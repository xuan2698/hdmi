def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # hh is BCD 12-hour: 0x12 = 12 o'clock, 0x01 = 1 o'clock
    # Initial state (power-up unspecified, but we need concrete values)
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

        # R1_reset: synchronous reset, priority over enable
        if reset == 1:
            ss_ones = 0
            ss_tens = 0
            mm_ones = 0
            mm_tens = 0
            hh_ones = 2
            hh_tens = 1
            pm_state = 0
        elif ena == 1:
            # R2_seconds / R3_seconds_rollover / R4_minutes_rollover / R5_hour_rollover_am_pm
            ss_val = ss_tens * 10 + ss_ones
            mm_val = mm_tens * 10 + mm_ones
            hh_val = hh_tens * 10 + hh_ones

            if ss_val != 59:
                # R2_seconds: increment seconds
                if ss_ones == 9:
                    ss_ones = 0
                    ss_tens += 1
                else:
                    ss_ones += 1
            else:
                # seconds rollover
                ss_ones = 0
                ss_tens = 0
                if mm_val != 59:
                    # R3_seconds_rollover: increment minutes
                    if mm_ones == 9:
                        mm_ones = 0
                        mm_tens += 1
                    else:
                        mm_ones += 1
                else:
                    # minutes rollover
                    mm_ones = 0
                    mm_tens = 0
                    if hh_val != 11:
                        # R4_minutes_rollover: increment hours (not 11 -> not 12)
                        if hh_val == 12:
                            hh_val = 1
                        else:
                            hh_val += 1
                        hh_tens = hh_val // 10
                        hh_ones = hh_val % 10
                    else:
                        # R5_hour_rollover_am_pm: 11 -> 12, toggle pm
                        hh_tens = 1
                        hh_ones = 2
                        pm_state = 1 - pm_state
        # R6_hold: ena==0 and reset==0 -> no change

        hh_out = (hh_tens << 4) | hh_ones
        mm_out = (mm_tens << 4) | mm_ones
        ss_out = (ss_tens << 4) | ss_ones

        results.append({
            'pm': pm_state,
            'hh': hh_out,
            'mm': mm_out,
            'ss': ss_out,
        })

    return results
