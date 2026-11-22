def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # Reset values: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
    ss_lo, ss_hi = 0, 0
    mm_lo, mm_hi = 0, 0
    hh_lo, hh_hi = 2, 1  # 0x12
    pm_reg = 0

    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Sample current outputs before edge
        ss = (ss_hi << 4) | ss_lo
        mm = (mm_hi << 4) | mm_lo
        hh = (hh_hi << 4) | hh_lo
        out.append({'pm': pm_reg, 'hh': hh, 'mm': mm, 'ss': ss})

        # Compute next state at posedge
        if reset:
            # R1_reset: synchronous reset to 12:00 AM
            ss_lo, ss_hi = 0, 0
            mm_lo, mm_hi = 0, 0
            hh_lo, hh_hi = 2, 1
            pm_reg = 0
        elif ena:
            # R2_hold: not enabled -> hold (handled by else)
            # R3_seconds: increment seconds unless 59
            if ss != 0x59:
                # increment BCD seconds
                if ss_lo == 9:
                    ss_lo = 0
                    ss_hi += 1
                else:
                    ss_lo += 1
            else:
                # R4_seconds_roll: seconds roll to 00, increment minutes unless 59
                ss_lo, ss_hi = 0, 0
                if mm != 0x59:
                    if mm_lo == 9:
                        mm_lo = 0
                        mm_hi += 1
                    else:
                        mm_lo += 1
                else:
                    # R5_minutes_roll: minutes roll to 00, increment hours
                    mm_lo, mm_hi = 0, 0
                    if hh == 0x12:
                        # R6_hour_roll_am_pm: 12 -> 1, toggle pm
                        hh_lo, hh_hi = 1, 0
                        pm_reg = 1 - pm_reg
                    elif hh == 0x11:
                        # R7_hour_roll_12: 11 -> 12, toggle pm
                        hh_lo, hh_hi = 2, 1
                        pm_reg = 1 - pm_reg
                    else:
                        # increment hours BCD (01..10)
                        if hh_lo == 9:
                            hh_lo = 0
                            hh_hi += 1
                        else:
                            hh_lo += 1
        # else: R2_hold - no change

    return out
