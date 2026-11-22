def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # Initialize to 12:00 AM (power-up unspecified, but we pick a concrete value)
    ss_ones, ss_tens = 0, 0
    mm_ones, mm_tens = 0, 0
    hh_ones, hh_tens = 2, 1  # 12
    pm_state = 0

    results = []
    for v in vectors:
        reset = v.get('reset', 0)
        ena = v.get('ena', 0)

        # R1_reset: synchronous reset to 12:00 AM, priority 1
        if reset == 1:
            ss_ones, ss_tens = 0, 0
            mm_ones, mm_tens = 0, 0
            hh_ones, hh_tens = 2, 1
            pm_state = 0
        elif ena == 1:
            # R2_seconds: increment seconds when not at 59
            ss_val = ss_tens * 10 + ss_ones
            if ss_val != 59:
                if ss_ones == 9:
                    ss_ones = 0
                    ss_tens += 1
                else:
                    ss_ones += 1
            else:
                # R3_seconds_rollover: ss==59, roll seconds to 00, increment minutes
                ss_ones, ss_tens = 0, 0
                mm_val = mm_tens * 10 + mm_ones
                if mm_val != 59:
                    if mm_ones == 9:
                        mm_ones = 0
                        mm_tens += 1
                    else:
                        mm_ones += 1
                else:
                    # R4_minutes_rollover: mm==59, roll minutes to 00, increment hours
                    mm_ones, mm_tens = 0, 0
                    hh_val = hh_tens * 10 + hh_ones
                    if hh_val != 12:
                        if hh_ones == 9:
                            hh_ones = 0
                            hh_tens += 1
                        else:
                            hh_ones += 1
                    else:
                        # R5_hour_rollover_am_pm: hh==12, roll to 01, toggle pm
                        hh_ones, hh_tens = 1, 0
                        pm_state = 1 - pm_state
        # R6_hold: ena==0 and reset==0, hold state (no change)

        hh = (hh_tens << 4) | hh_ones
        mm = (mm_tens << 4) | mm_ones
        ss = (ss_tens << 4) | ss_ones
        results.append({'pm': pm_state, 'hh': hh, 'mm': mm, 'ss': ss})

    return results
