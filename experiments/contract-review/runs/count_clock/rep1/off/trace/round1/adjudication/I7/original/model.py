def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # Initialize to 12:00 AM (hh=0x12, mm=0x00, ss=0x00, pm=0)
    ss_lo, ss_hi = 0, 0
    mm_lo, mm_hi = 0, 0
    hh_lo, hh_hi = 2, 1  # 0x12
    pm_reg = 0

    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Compute next state based on current state and inputs (sampled at posedge)
        if reset:
            # R1_reset: reset to 12:00 AM
            n_ss_lo, n_ss_hi = 0, 0
            n_mm_lo, n_mm_hi = 0, 0
            n_hh_lo, n_hh_hi = 2, 1
            n_pm = 0
        elif not ena:
            # R2_hold
            n_ss_lo, n_ss_hi = ss_lo, ss_hi
            n_mm_lo, n_mm_hi = mm_lo, mm_hi
            n_hh_lo, n_hh_hi = hh_lo, hh_hi
            n_pm = pm_reg
        else:
            # ena == 1, reset == 0
            ss = (ss_hi << 4) | ss_lo
            mm = (mm_hi << 4) | mm_lo
            hh = (hh_hi << 4) | hh_lo

            if ss != 0x59:
                # R3_seconds: increment seconds
                n_ss_lo, n_ss_hi = ss_lo, ss_hi
                if ss_lo == 9:
                    n_ss_lo = 0
                    n_ss_hi = ss_hi + 1
                else:
                    n_ss_lo = ss_lo + 1
                n_mm_lo, n_mm_hi = mm_lo, mm_hi
                n_hh_lo, n_hh_hi = hh_lo, hh_hi
                n_pm = pm_reg
            elif mm != 0x59:
                # R4_seconds_roll: seconds roll to 00, minutes increment
                n_ss_lo, n_ss_hi = 0, 0
                if mm_lo == 9:
                    n_mm_lo = 0
                    n_mm_hi = mm_hi + 1
                else:
                    n_mm_lo = mm_lo + 1
                    n_mm_hi = mm_hi
                n_hh_lo, n_hh_hi = hh_lo, hh_hi
                n_pm = pm_reg
            elif not (hh == 0x11 and pm_reg == 0):
                # R5_minutes_roll: seconds and minutes roll, hours increment
                n_ss_lo, n_ss_hi = 0, 0
                n_mm_lo, n_mm_hi = 0, 0
                # increment hours
                if hh_lo == 9:
                    n_hh_lo = 0
                    n_hh_hi = hh_hi + 1
                elif hh_lo == 2 and hh_hi == 1:
                    # 12 -> 01
                    n_hh_lo = 1
                    n_hh_hi = 0
                else:
                    n_hh_lo = hh_lo + 1
                    n_hh_hi = hh_hi
                n_pm = pm_reg
            elif pm_reg == 0:
                # R6_hours_roll_am_to_pm: 11:59:59 AM -> 12:00:00 PM
                n_ss_lo, n_ss_hi = 0, 0
                n_mm_lo, n_mm_hi = 0, 0
                n_hh_lo, n_hh_hi = 2, 1  # 12
                n_pm = 1
            else:
                # R7_hours_roll_pm_to_am: 11:59:59 PM -> 12:00:00 AM
                n_ss_lo, n_ss_hi = 0, 0
                n_mm_lo, n_mm_hi = 0, 0
                n_hh_lo, n_hh_hi = 2, 1  # 12
                n_pm = 0

        # Output current state (before edge) - values driven before sampled edge
        out.append({
            'pm': pm_reg,
            'hh': (hh_hi << 4) | hh_lo,
            'mm': (mm_hi << 4) | mm_lo,
            'ss': (ss_hi << 4) | ss_lo,
        })

        # Apply next state
        ss_lo, ss_hi = n_ss_lo, n_ss_hi
        mm_lo, mm_hi = n_mm_lo, n_mm_hi
        hh_lo, hh_hi = n_hh_lo, n_hh_hi
        pm_reg = n_pm

    return out
