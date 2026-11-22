def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # hh is BCD 12-hour: 0x12 = 12 o'clock, 0x01 = 1 o'clock, etc.
    # Initial state: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
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

        # Compute next state at posedge clk
        if reset == 1:
            # R1_reset: reset has priority, sets to 12:00 AM
            ss_ones = 0
            ss_tens = 0
            mm_ones = 0
            mm_tens = 0
            hh_ones = 2
            hh_tens = 1
            pm_state = 0
        elif ena == 1:
            # R2_seconds / R3_seconds_rollover / R4_minutes_rollover / R5_hour_rollover_am_pm
            ss_val = (ss_tens << 4) | ss_ones
            mm_val = (mm_tens << 4) | mm_ones
            hh_val = (hh_tens << 4) | hh_ones

            if ss_val != 0x59:
                # R2_seconds: increment seconds
                if ss_ones == 9:
                    ss_ones = 0
                    ss_tens += 1
                else:
                    ss_ones += 1
            else:
                # ss == 0x59
                ss_ones = 0
                ss_tens = 0
                if mm_val != 0x59:
                    # R3_seconds_rollover: increment minutes
                    if mm_ones == 9:
                        mm_ones = 0
                        mm_tens += 1
                    else:
                        mm_ones += 1
                else:
                    # mm == 0x59
                    mm_ones = 0
                    mm_tens = 0
                    if hh_val != 0x12:
                        # R4_minutes_rollover: increment hours (not 12 -> 1)
                        # hh is BCD 12-hour: 01..12
                        if hh_val == 0x09:
                            hh_ones = 0
                            hh_tens = 1
                        elif hh_val == 0x11:
                            hh_ones = 2
                            hh_tens = 1
                        else:
                            hh_ones += 1
                    else:
                        # R5_hour_rollover_am_pm: 12 -> 1, toggle pm
                        hh_ones = 1
                        hh_tens = 0
                        pm_state = 1 - pm_state
        # else: R6_hold: ena == 0, no change

    return results
