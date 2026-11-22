def reference(vectors):
    # Contract rules implemented:
    # R1_reset: synchronous active-high reset -> 12:00 AM (pm=0, hh=0x12, mm=0x00, ss=0x00)
    # R2_seconds: ena increments seconds when ss != 0x59
    # R3_seconds_rollover: ss==0x59 and mm!=0x59 -> ss=0, mm+1
    # R4_minutes_rollover: ss==0x59 and mm==0x59 and hh!=0x12 -> ss=0, mm=0, hh+1
    # R5_hour_rollover_am_pm: ss==0x59 and mm==0x59 and hh==0x12 -> ss=0, mm=0, hh=1, pm toggles
    # R6_hold: ena==0 and reset==0 -> hold all outputs

    # State: BCD digits
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

        # Sample current outputs (before edge)
        results.append({
            'pm': pm_state,
            'hh': bcd(hh_tens, hh_ones),
            'mm': bcd(mm_tens, mm_ones),
            'ss': bcd(ss_tens, ss_ones),
        })

        # Compute next state at posedge
        if reset == 1:
            # R1_reset
            ss_ones = 0
            ss_tens = 0
            mm_ones = 0
            mm_tens = 0
            hh_ones = 2
            hh_tens = 1
            pm_state = 0
        elif ena == 1:
            ss_val = bcd(ss_tens, ss_ones)
            mm_val = bcd(mm_tens, mm_ones)
            hh_val = bcd(hh_tens, hh_ones)
            if ss_val != 0x59:
                # R2_seconds
                if ss_ones == 9:
                    ss_ones = 0
                    ss_tens += 1
                else:
                    ss_ones += 1
            elif mm_val != 0x59:
                # R3_seconds_rollover
                ss_ones = 0
                ss_tens = 0
                if mm_ones == 9:
                    mm_ones = 0
                    mm_tens += 1
                else:
                    mm_ones += 1
            elif hh_val != 0x12:
                # R4_minutes_rollover
                ss_ones = 0
                ss_tens = 0
                mm_ones = 0
                mm_tens = 0
                if hh_ones == 9:
                    hh_ones = 0
                    hh_tens += 1
                else:
                    hh_ones += 1
            else:
                # R5_hour_rollover_am_pm
                ss_ones = 0
                ss_tens = 0
                mm_ones = 0
                mm_tens = 0
                hh_ones = 1
                hh_tens = 0
                pm_state = 1 - pm_state
        # else: R6_hold (no change)

    return results
