def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # BCD digits stored as integers 0-9.
    # Initial (power-up) state: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
    ss_lo = 0
    ss_hi = 0
    mm_lo = 0
    mm_hi = 0
    hh_lo = 2
    hh_hi = 1
    pm_reg = 0

    out = []
    for row in vectors:
        # Sample inputs at posedge (values driven before edge)
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # R1_reset: synchronous reset, priority 1
        if reset == 1:
            ss_lo = 0
            ss_hi = 0
            mm_lo = 0
            mm_hi = 0
            hh_lo = 2
            hh_hi = 1
            pm_reg = 0
        # R2_hold: no enable, hold
        elif ena == 0:
            pass
        else:
            # ena == 1, not reset: increment
            # R3_seconds: increment seconds if ss != 0x59
            if not (ss_hi == 5 and ss_lo == 9):
                if ss_lo == 9:
                    ss_lo = 0
                    ss_hi += 1
                else:
                    ss_lo += 1
            else:
                # ss == 0x59: roll seconds, increment minutes
                ss_lo = 0
                ss_hi = 0
                # R4_seconds_roll: if mm != 0x59, increment minutes
                if not (mm_hi == 5 and mm_lo == 9):
                    if mm_lo == 9:
                        mm_lo = 0
                        mm_hi += 1
                    else:
                        mm_lo += 1
                else:
                    # mm == 0x59: roll minutes, increment hours
                    mm_lo = 0
                    mm_hi = 0
                    # R5_minutes_roll / R6 / R7: hours roll
                    if hh_hi == 1 and hh_lo == 1:
                        # hh == 0x11 (12)
                        if pm_reg == 0:
                            # R6_hours_roll_am_to_pm: 12:00 AM -> 12:00 PM
                            pm_reg = 1
                            hh_hi = 1
                            hh_lo = 2
                        else:
                            # R7_hours_roll_pm_to_am: 12:00 PM -> 12:00 AM
                            pm_reg = 0
                            hh_hi = 1
                            hh_lo = 2
                    else:
                        # R5_minutes_roll: increment hours normally
                        if hh_lo == 9:
                            hh_lo = 0
                            hh_hi += 1
                        else:
                            hh_lo += 1

        # Outputs (BCD packed: hi nibble = tens, lo nibble = ones)
        hh = (hh_hi << 4) | hh_lo
        mm = (mm_hi << 4) | mm_lo
        ss = (ss_hi << 4) | ss_lo
        out.append({'pm': pm_reg, 'hh': hh, 'mm': mm, 'ss': ss})

    return out
