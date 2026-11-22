def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # BCD digits. hh is 01-12, with 12 represented as hh_hi=1, hh_lo=2.
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

        # R1_reset: synchronous reset has priority, sets 12:00 AM
        if reset == 1:
            ss_lo = 0; ss_hi = 0
            mm_lo = 0; mm_hi = 0
            hh_lo = 2; hh_hi = 1
            pm_reg = 0
        # R2_hold: no enable, hold state
        elif ena == 0:
            pass
        else:
            # ena == 1, reset == 0: increment
            ss = ss_hi * 10 + ss_lo
            mm = mm_hi * 10 + mm_lo
            hh = hh_hi * 10 + hh_lo

            # R3_seconds: increment seconds if not 59
            if ss != 59:
                ss_lo += 1
                if ss_lo == 10:
                    ss_lo = 0
                    ss_hi += 1
            else:
                # R4_seconds_roll: ss==59, roll seconds, increment minutes if mm!=59
                ss_lo = 0; ss_hi = 0
                if mm != 59:
                    mm_lo += 1
                    if mm_lo == 10:
                        mm_lo = 0
                        mm_hi += 1
                else:
                    # R5_minutes_roll: mm==59, roll minutes, increment hours
                    mm_lo = 0; mm_hi = 0
                    if hh == 11 and pm_reg == 0:
                        # R6_hours_roll_am_to_pm: 11:59:59 AM -> 12:00:00 PM
                        hh_lo = 2; hh_hi = 1
                        pm_reg = 1
                    elif hh == 11 and pm_reg == 1:
                        # R7_hours_roll_pm_to_am: 11:59:59 PM -> 12:00:00 AM
                        hh_lo = 2; hh_hi = 1
                        pm_reg = 0
                    else:
                        # Normal hour increment 01..10, 12 handled above
                        hh += 1
                        if hh == 13:
                            hh = 1
                        hh_hi = hh // 10
                        hh_lo = hh % 10

        hh_val = hh_hi * 10 + hh_lo
        mm_val = mm_hi * 10 + mm_lo
        ss_val = ss_hi * 10 + ss_lo

        out.append({
            'pm': pm_reg & 1,
            'hh': ((hh_hi << 4) | hh_lo) & 0xFF,
            'mm': ((mm_hi << 4) | mm_lo) & 0xFF,
            'ss': ((ss_hi << 4) | ss_lo) & 0xFF,
        })
    return out
