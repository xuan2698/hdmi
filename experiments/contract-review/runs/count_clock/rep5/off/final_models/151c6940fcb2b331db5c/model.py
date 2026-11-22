def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # Initial state: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
    ss_ones = 0
    ss_tens = 0
    mm_ones = 0
    mm_tens = 0
    hh_ones = 2
    hh_tens = 1
    pm_state = 0

    def pack(tens, ones):
        return (tens << 4) | ones

    results = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Sample outputs before edge (current state)
        results.append({
            'pm': pm_state,
            'hh': pack(hh_tens, hh_ones),
            'mm': pack(mm_tens, mm_ones),
            'ss': pack(ss_tens, ss_ones),
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
            ss_val = pack(ss_tens, ss_ones)
            mm_val = pack(mm_tens, mm_ones)
            hh_val = pack(hh_tens, hh_ones)
            if ss_val != 0x59:
                # R2_seconds: increment seconds
                if ss_ones == 9:
                    ss_ones = 0
                    ss_tens += 1
                else:
                    ss_ones += 1
            elif mm_val != 0x59:
                # R3_seconds_rollover: ss=59, mm!=59 -> ss=00, mm++
                ss_ones = 0
                ss_tens = 0
                if mm_ones == 9:
                    mm_ones = 0
                    mm_tens += 1
                else:
                    mm_ones += 1
            elif hh_val != 0x12:
                # R4_minutes_rollover: ss=59, mm=59, hh!=12 -> mm=00, hh++
                ss_ones = 0
                ss_tens = 0
                mm_ones = 0
                mm_tens = 0
                if hh_val == 0x09:
                    hh_ones = 0
                    hh_tens = 1
                elif hh_val == 0x11:
                    hh_ones = 2
                    hh_tens = 1
                else:
                    hh_ones += 1
            else:
                # R5_hour_rollover_am_pm: ss=59, mm=59, hh=12 -> hh=01, mm=00, ss=00, toggle pm
                ss_ones = 0
                ss_tens = 0
                mm_ones = 0
                mm_tens = 0
                hh_ones = 1
                hh_tens = 0
                pm_state = 1 - pm_state
        # else: R6_hold: no change

    return results
