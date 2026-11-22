def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # BCD encoded outputs
    ss_lo = 0
    ss_hi = 0
    mm_lo = 0
    mm_hi = 0
    hh_lo = 2
    hh_hi = 1
    pm_reg = 0

    def pack(hi, lo):
        return (hi << 4) | lo

    results = []
    for vec in vectors:
        reset = vec.get('reset', 0)
        ena = vec.get('ena', 0)

        # R1_reset: synchronous reset to 12:00 AM, priority 1
        if reset == 1:
            ss_lo = 0
            ss_hi = 0
            mm_lo = 0
            mm_hi = 0
            hh_lo = 2
            hh_hi = 1
            pm_reg = 0
        # R2_hold: no enable, hold state, priority 2
        elif ena == 0:
            pass
        else:
            # ena == 1, reset == 0: increment
            ss = pack(ss_hi, ss_lo)
            mm = pack(mm_hi, mm_lo)
            hh = pack(hh_hi, hh_lo)

            # R3_seconds: increment seconds if not 59
            if ss != 0x59:
                ss_lo += 1
                if ss_lo == 10:
                    ss_lo = 0
                    ss_hi += 1
            else:
                # R4_seconds_roll: seconds roll to 00, increment minutes if not 59
                ss_lo = 0
                ss_hi = 0
                if mm != 0x59:
                    mm_lo += 1
                    if mm_lo == 10:
                        mm_lo = 0
                        mm_hi += 1
                else:
                    # R5_minutes_roll: minutes roll to 00, increment hours if not 12
                    mm_lo = 0
                    mm_hi = 0
                    if hh != 0x12:
                        # R7_hour_roll_12: if hh == 11, roll to 12 and toggle pm
                        if hh == 0x11:
                            hh_lo = 2
                            hh_hi = 1
                            pm_reg = 1 - pm_reg
                        else:
                            hh_lo += 1
                            if hh_lo == 10:
                                hh_lo = 0
                                hh_hi += 1
                    else:
                        # R6_hour_roll_am_pm: hh == 12, roll to 01 and toggle pm
                        hh_lo = 1
                        hh_hi = 0
                        pm_reg = 1 - pm_reg

        results.append({
            'pm': pm_reg,
            'hh': pack(hh_hi, hh_lo),
            'mm': pack(mm_hi, mm_lo),
            'ss': pack(ss_hi, ss_lo),
        })

    return results
