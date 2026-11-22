def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # BCD encoded outputs. Reset value: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
    # R1_reset: reset==1 -> next cycle pm=0, hh=0x12, mm=0, ss=0
    # R2_hold: reset==0 && ena==0 -> hold
    # R3_seconds: ena && ss!=0x59 -> ss+1 (BCD)
    # R4_seconds_roll: ena && ss==0x59 && mm!=0x59 -> ss=0, mm+1 (BCD)
    # R5_minutes_roll: ena && ss==0x59 && mm==0x59 && hh!=0x12 -> ss=0, mm=0, hh+1 (BCD, 01..12)
    # R6_hours_roll_am_pm: ena && ss==0x59 && mm==0x59 && hh==0x12 -> ss=0, mm=0, hh=0x01, pm toggles

    # Initialize state to reset value (power-up unspecified but we use reset value)
    ss = 0x00
    mm = 0x00
    hh = 0x12
    pm = 0

    results = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Compute next state based on current state and inputs (sampled at posedge)
        if reset == 1:
            # R1_reset
            n_ss = 0x00
            n_mm = 0x00
            n_hh = 0x12
            n_pm = 0
        elif ena == 0:
            # R2_hold
            n_ss = ss
            n_mm = mm
            n_hh = hh
            n_pm = pm
        else:
            # ena == 1, reset == 0
            if ss != 0x59:
                # R3_seconds
                ss_lo = ss & 0x0F
                ss_hi = (ss >> 4) & 0x0F
                ss_lo += 1
                if ss_lo == 10:
                    ss_lo = 0
                    ss_hi += 1
                n_ss = (ss_hi << 4) | ss_lo
                n_mm = mm
                n_hh = hh
                n_pm = pm
            elif mm != 0x59:
                # R4_seconds_roll
                n_ss = 0x00
                mm_lo = mm & 0x0F
                mm_hi = (mm >> 4) & 0x0F
                mm_lo += 1
                if mm_lo == 10:
                    mm_lo = 0
                    mm_hi += 1
                n_mm = (mm_hi << 4) | mm_lo
                n_hh = hh
                n_pm = pm
            elif hh != 0x12:
                # R5_minutes_roll
                n_ss = 0x00
                n_mm = 0x00
                hh_lo = hh & 0x0F
                hh_hi = (hh >> 4) & 0x0F
                hh_lo += 1
                if hh_lo == 10:
                    hh_lo = 0
                    hh_hi += 1
                n_hh = (hh_hi << 4) | hh_lo
                n_pm = pm
            else:
                # R6_hours_roll_am_pm: hh == 0x12
                n_ss = 0x00
                n_mm = 0x00
                n_hh = 0x01
                n_pm = 1 - pm

        # Outputs are the current state (before edge) - but contract says visible next_cycle
        # The expected outputs in examples show the state AFTER the edge.
        # We output the next state values.
        results.append({
            'pm': n_pm,
            'hh': n_hh,
            'mm': n_mm,
            'ss': n_ss
        })

        # Update state
        ss = n_ss
        mm = n_mm
        hh = n_hh
        pm = n_pm

    return results
