def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # Initialize to 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
    ss_ones = 0
    ss_tens = 0
    mm_ones = 0
    mm_tens = 0
    hh_ones = 2
    hh_tens = 1
    pm_state = 0

    results = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Outputs are driven before the sampled edge (current state)
        results.append({
            'pm': pm_state,
            'hh': (hh_tens << 4) | hh_ones,
            'mm': (mm_tens << 4) | mm_ones,
            'ss': (ss_tens << 4) | ss_ones,
        })

        # Compute next state at posedge
        if reset == 1:
            # R1_reset: reset to 12:00 AM
            ss_ones = 0
            ss_tens = 0
            mm_ones = 0
            mm_tens = 0
            hh_ones = 2
            hh_tens = 1
            pm_state = 0
        elif ena == 1:
            # R2_seconds / R3_seconds_rollover / R4_minutes_rollover / R5_hour_rollover_am_pm
            if ss_ones != 9:
                ss_ones += 1
            else:
                ss_ones = 0
                if ss_tens != 5:
                    ss_tens += 1
                else:
                    ss_tens = 0
                    # seconds rolled over to 00, increment minutes
                    if mm_ones != 9:
                        mm_ones += 1
                    else:
                        mm_ones = 0
                        if mm_tens != 5:
                            mm_tens += 1
                        else:
                            mm_tens = 0
                            # minutes rolled over to 00, increment hours
                            # current hour value
                            cur_hh = (hh_tens << 4) | hh_ones
                            if cur_hh == 0x11:
                                # 11 -> 12, pm unchanged
                                hh_tens = 1
                                hh_ones = 2
                            elif cur_hh == 0x12:
                                # 12 -> 01, toggle pm
                                hh_tens = 0
                                hh_ones = 1
                                pm_state = 1 - pm_state
                            else:
                                # 01..10 -> increment
                                if hh_ones != 9:
                                    hh_ones += 1
                                else:
                                    hh_ones = 0
                                    hh_tens += 1
        # else R6_hold: no change

    return results
