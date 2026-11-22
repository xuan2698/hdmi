def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # Initial state: 12:00 AM -> hh=12, mm=00, ss=00, pm=0
    # hh is BCD: hh_tens=1, hh_ones=2
    ss_ones = 0
    ss_tens = 0
    mm_ones = 0
    mm_tens = 0
    hh_ones = 2
    hh_tens = 1
    pm_state = 0

    def bcd(tens, ones):
        return (tens << 4) | ones

    results = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # R1_reset: synchronous reset to 12:00 AM, priority 1
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
            ss_val = bcd(ss_tens, ss_ones)
            mm_val = bcd(mm_tens, mm_ones)
            hh_val = bcd(hh_tens, hh_ones)

            if ss_val != 0x59:
                # R2_seconds: increment seconds
                if ss_ones == 9:
                    ss_ones = 0
                    ss_tens += 1
                else:
                    ss_ones += 1
            else:
                # ss == 59
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
                    # mm == 59
                    mm_ones = 0
                    mm_tens = 0
                    if hh_val != 0x12:
                        # R4_minutes_rollover: increment hours (not 12)
                        if hh_ones == 9:
                            hh_ones = 0
                            hh_tens += 1
                        else:
                            hh_ones += 1
                    else:
                        # R5_hour_rollover_am_pm: hh == 12, roll to 1 and toggle pm
                        hh_tens = 0
                        hh_ones = 1
                        pm_state = 1 - pm_state
        # R6_hold: ena == 0 and reset == 0 -> no change

        results.append({
            'pm': pm_state,
            'hh': bcd(hh_tens, hh_ones),
            'mm': bcd(mm_tens, mm_ones),
            'ss': bcd(ss_tens, ss_ones),
        })

    return results
