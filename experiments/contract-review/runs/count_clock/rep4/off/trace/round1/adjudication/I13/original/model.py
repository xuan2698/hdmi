def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # BCD digits. hh is 01-12.
    # Initialize to 12:00 AM (hh=0x12, mm=0x00, ss=0x00, pm=0)
    ss_lo = 0
    ss_hi = 0
    mm_lo = 0
    mm_hi = 0
    hh_lo = 2
    hh_hi = 1
    pm_reg = 0

    results = []
    for vec in vectors:
        reset = vec.get('reset', 0)
        ena = vec.get('ena', 0)

        # Compute next state based on current state and inputs (posedge sampling)
        if reset:
            # R1_reset: synchronous reset to 12:00 AM
            n_ss_lo, n_ss_hi = 0, 0
            n_mm_lo, n_mm_hi = 0, 0
            n_hh_lo, n_hh_hi = 2, 1
            n_pm = 0
        elif not ena:
            # R2_hold: hold state
            n_ss_lo, n_ss_hi = ss_lo, ss_hi
            n_mm_lo, n_mm_hi = mm_lo, mm_hi
            n_hh_lo, n_hh_hi = hh_lo, hh_hi
            n_pm = pm_reg
        else:
            # ena == 1, increment
            ss_val = ss_hi * 10 + ss_lo
            mm_val = mm_hi * 10 + mm_lo
            hh_val = hh_hi * 10 + hh_lo

            if ss_val != 59:
                # R3_seconds: increment seconds
                n_ss_lo, n_ss_hi = ss_lo, ss_hi
                n_mm_lo, n_mm_hi = mm_lo, mm_hi
                n_hh_lo, n_hh_hi = hh_lo, hh_hi
                n_pm = pm_reg
                ns = ss_val + 1
                n_ss_lo = ns % 10
                n_ss_hi = ns // 10
            elif mm_val != 59:
                # R4_seconds_roll: seconds roll to 00, minutes increment
                n_ss_lo, n_ss_hi = 0, 0
                n_hh_lo, n_hh_hi = hh_lo, hh_hi
                n_pm = pm_reg
                nm = mm_val + 1
                n_mm_lo = nm % 10
                n_mm_hi = nm // 10
            elif hh_val != 12:
                # R5_minutes_roll: minutes roll to 00, hours increment
                n_ss_lo, n_ss_hi = 0, 0
                n_mm_lo, n_mm_hi = 0, 0
                n_pm = pm_reg
                nh = hh_val + 1
                n_hh_lo = nh % 10
                n_hh_hi = nh // 10
            else:
                # hh_val == 12
                # R6_hour_roll_am_pm: 12 -> 1, toggle pm
                n_ss_lo, n_ss_hi = 0, 0
                n_mm_lo, n_mm_hi = 0, 0
                n_hh_lo, n_hh_hi = 1, 0
                n_pm = 1 - pm_reg

        # Outputs are driven before the sampled edge (current state)
        # R7_hour_roll_12 is covered by R5/R6 logic (11->12 handled by R5 since hh!=12)
        hh_out = (hh_hi << 4) | hh_lo
        mm_out = (mm_hi << 4) | mm_lo
        ss_out = (ss_hi << 4) | ss_lo
        results.append({
            'pm': pm_reg,
            'hh': hh_out,
            'mm': mm_out,
            'ss': ss_out
        })

        # Advance state
        ss_lo, ss_hi = n_ss_lo, n_ss_hi
        mm_lo, mm_hi = n_mm_lo, n_mm_hi
        hh_lo, hh_hi = n_hh_lo, n_hh_hi
        pm_reg = n_pm

    return results
