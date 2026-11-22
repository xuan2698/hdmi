def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # BCD encoding: value = hi*10 + lo
    # Reset value: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
    ss_lo = 0
    ss_hi = 0
    mm_lo = 0
    mm_hi = 0
    hh_lo = 2
    hh_hi = 1
    pm_reg = 0

    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Sample outputs BEFORE edge (values driven before sampled edge)
        out.append({
            'pm': pm_reg,
            'hh': (hh_hi << 4) | hh_lo,
            'mm': (mm_hi << 4) | mm_lo,
            'ss': (ss_hi << 4) | ss_lo,
        })

        # Compute next state at posedge
        if reset == 1:
            # R1_reset: synchronous reset to 12:00 AM, priority over ena
            ss_lo = 0
            ss_hi = 0
            mm_lo = 0
            mm_hi = 0
            hh_lo = 2
            hh_hi = 1
            pm_reg = 0
        elif ena == 0:
            # R2_hold: hold all state
            pass
        else:
            # ena == 1, reset == 0
            ss_val = ss_hi * 10 + ss_lo
            mm_val = mm_hi * 10 + mm_lo
            hh_val = hh_hi * 10 + hh_lo

            if ss_val != 59:
                # R3_seconds: increment seconds
                ss_val += 1
                ss_lo = ss_val % 10
                ss_hi = ss_val // 10
            else:
                # seconds roll over
                ss_lo = 0
                ss_hi = 0
                if mm_val != 59:
                    # R4_seconds_roll: increment minutes
                    mm_val += 1
                    mm_lo = mm_val % 10
                    mm_hi = mm_val // 10
                else:
                    # minutes roll over
                    mm_lo = 0
                    mm_hi = 0
                    if hh_val != 12:
                        # R5_minutes_roll: increment hours (not 12)
                        hh_val += 1
                        hh_lo = hh_val % 10
                        hh_hi = hh_val // 10
                    else:
                        # hh == 12
                        if pm_reg == 0:
                            # R6_hour_roll_am_pm: 12 AM -> 1 PM
                            pm_reg = 1
                            hh_lo = 1
                            hh_hi = 0
                        else:
                            # R7_hour_roll_12: 12 PM -> 1 AM
                            pm_reg = 0
                            hh_lo = 1
                            hh_hi = 0

    return out
