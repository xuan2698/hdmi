def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # BCD encoded. hh in 01..12 (0x01..0x12), mm/ss in 00..59.
    # R1_reset: reset==1 -> pm=0, hh=0x12, mm=0, ss=0
    # R2_hold: reset==0 && ena==0 -> hold
    # R3_seconds: ena && ss!=0x59 -> ss++
    # R4_seconds_roll: ena && ss==0x59 && mm!=0x59 -> ss=0, mm++
    # R5_minutes_roll: ena && ss==0x59 && mm==0x59 && hh!=0x12 -> ss=0,mm=0,hh++
    # R6_hour_roll_am_pm: ena && ss==0x59 && mm==0x59 && hh==0x12 -> ss=0,mm=0,hh=0x01,pm^=1
    # R7_hour_roll_12: ena && ss==0x59 && mm==0x59 && hh==0x11 -> ss=0,mm=0,hh=0x12,pm^=1

    # Initialize state (power-up unspecified; use reset values as concrete)
    ss_lo = 0
    ss_hi = 0
    mm_lo = 0
    mm_hi = 0
    hh_lo = 2
    hh_hi = 1
    pm_reg = 0

    def bcd(hi, lo):
        return (hi << 4) | lo

    def inc_bcd(hi, lo, max_hi, max_lo):
        # increment BCD digit pair
        if lo < max_lo:
            return hi, lo + 1
        else:
            return hi + 1, 0

    results = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Sample current outputs BEFORE edge (values driven before sampled edge)
        # Actually: "Each row's values are driven before the sampled edge."
        # So outputs reflect state before this posedge.
        out = {
            'pm': pm_reg,
            'hh': bcd(hh_hi, hh_lo),
            'mm': bcd(mm_hi, mm_lo),
            'ss': bcd(ss_hi, ss_lo),
        }
        results.append(out)

        # Compute next state at posedge
        if reset == 1:
            # R1_reset
            ss_lo = 0; ss_hi = 0
            mm_lo = 0; mm_hi = 0
            hh_lo = 2; hh_hi = 1
            pm_reg = 0
        elif ena == 0:
            # R2_hold
            pass
        else:
            # ena == 1
            ss_val = bcd(ss_hi, ss_lo)
            mm_val = bcd(mm_hi, mm_lo)
            hh_val = bcd(hh_hi, hh_lo)

            if ss_val != 0x59:
                # R3_seconds
                ss_hi, ss_lo = inc_bcd(ss_hi, ss_lo, 5, 9)
            elif mm_val != 0x59:
                # R4_seconds_roll
                ss_hi = 0; ss_lo = 0
                mm_hi, mm_lo = inc_bcd(mm_hi, mm_lo, 5, 9)
            elif hh_val == 0x12:
                # R6_hour_roll_am_pm
                ss_hi = 0; ss_lo = 0
                mm_hi = 0; mm_lo = 0
                hh_hi = 0; hh_lo = 1
                pm_reg = 1 - pm_reg
            elif hh_val == 0x11:
                # R7_hour_roll_12
                ss_hi = 0; ss_lo = 0
                mm_hi = 0; mm_lo = 0
                hh_hi = 1; hh_lo = 2
                pm_reg = 1 - pm_reg
            else:
                # R5_minutes_roll (hh != 0x12, and hh != 0x11 handled above)
                ss_hi = 0; ss_lo = 0
                mm_hi = 0; mm_lo = 0
                hh_hi, hh_lo = inc_bcd(hh_hi, hh_lo, 1, 9)

    return results
