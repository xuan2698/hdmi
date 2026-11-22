def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
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

        # R1_reset: synchronous reset, priority 1, visible next cycle
        if reset == 1:
            ss_lo = 0
            ss_hi = 0
            mm_lo = 0
            mm_hi = 0
            hh_lo = 2
            hh_hi = 1
            pm_reg = 0
        # R2_hold: no enable, no reset -> hold
        elif ena == 0:
            pass
        else:
            # ena == 1, reset == 0: increment
            ss_val = ss_hi * 10 + ss_lo
            mm_val = mm_hi * 10 + mm_lo
            hh_val = hh_hi * 10 + hh_lo

            if ss_val != 59:
                # R3_seconds: increment seconds
                ss_val += 1
                ss_lo = ss_val % 10
                ss_hi = ss_val // 10
            else:
                # seconds roll to 00
                ss_lo = 0
                ss_hi = 0
                if mm_val != 59:
                    # R4_seconds_roll: increment minutes
                    mm_val += 1
                    mm_lo = mm_val % 10
                    mm_hi = mm_val // 10
                else:
                    # minutes roll to 00
                    mm_lo = 0
                    mm_hi = 0
                    if hh_val != 12:
                        # R5_minutes_roll: increment hours
                        hh_val += 1
                        hh_lo = hh_val % 10
                        hh_hi = hh_val // 10
                    else:
                        # R6_hours_roll_am_pm: 12 -> 1, toggle pm
                        # Candidate interpretation: toggle pm at 11:59:59 -> 12:00:00
                        # Treat 12:00 AM as noon (12:00 PM) and toggle pm at 11:59:59.
                        hh_lo = 1
                        hh_hi = 0
                        pm_reg = 1 - pm_reg

        hh = (hh_hi << 4) | hh_lo
        mm = (mm_hi << 4) | mm_lo
        ss = (ss_hi << 4) | ss_lo
        out.append({'pm': pm_reg, 'hh': hh, 'mm': mm, 'ss': ss})

    return out
