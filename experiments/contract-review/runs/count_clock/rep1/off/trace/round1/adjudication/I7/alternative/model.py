def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # BCD digits. hh is 01-12.
    # R1_reset: reset==1 -> pm=0, hh=0x12, mm=0x00, ss=0x00
    # R2_hold: reset==0 && ena==0 -> hold
    # R3_seconds: ena && ss != 0x59 -> increment ss
    # R4_seconds_roll: ena && ss==0x59 && mm!=0x59 -> ss=0, mm++
    # R5_minutes_roll: ena && ss==0x59 && mm==0x59 && !(hh==0x11 && pm==0) -> ss=0,mm=0,hh++
    #   with interpretation: if hh==0x12 -> hh=0x01 (not 0x13)
    # R6_hours_roll_am_to_pm: ena && ss==0x59 && mm==0x59 && hh==0x11 && pm==0 -> ss=0,mm=0,hh=0x12,pm=1
    # R7_hours_roll_pm_to_am: ena && ss==0x59 && mm==0x59 && hh==0x11 && pm==1 -> ss=0,mm=0,hh=0x12,pm=0

    # Initialize state to reset values (power-up unspecified but we start at reset state)
    ss = 0x00
    mm = 0x00
    hh = 0x12
    pm = 0

    out = []
    for v in vectors:
        reset = v.get('reset', 0)
        ena = v.get('ena', 0)

        # Compute next state based on current state and inputs
        if reset == 1:
            # R1_reset
            n_ss, n_mm, n_hh, n_pm = 0x00, 0x00, 0x12, 0
        elif ena == 0:
            # R2_hold
            n_ss, n_mm, n_hh, n_pm = ss, mm, hh, pm
        else:
            # ena == 1, reset == 0
            if ss != 0x59:
                # R3_seconds
                ss_lo = ss & 0x0F
                ss_hi = (ss >> 4) & 0x0F
                ss_lo += 1
                if ss_lo > 9:
                    ss_lo = 0
                    ss_hi += 1
                n_ss = (ss_hi << 4) | ss_lo
                n_mm, n_hh, n_pm = mm, hh, pm
            elif mm != 0x59:
                # R4_seconds_roll
                n_ss = 0x00
                mm_lo = mm & 0x0F
                mm_hi = (mm >> 4) & 0x0F
                mm_lo += 1
                if mm_lo > 9:
                    mm_lo = 0
                    mm_hi += 1
                n_mm = (mm_hi << 4) | mm_lo
                n_hh, n_pm = hh, pm
            else:
                # ss==0x59 && mm==0x59
                if hh == 0x11 and pm == 0:
                    # R6_hours_roll_am_to_pm
                    n_ss, n_mm, n_hh, n_pm = 0x00, 0x00, 0x12, 1
                elif hh == 0x11 and pm == 1:
                    # R7_hours_roll_pm_to_am
                    n_ss, n_mm, n_hh, n_pm = 0x00, 0x00, 0x12, 0
                else:
                    # R5_minutes_roll
                    n_ss, n_mm = 0x00, 0x00
                    hh_lo = hh & 0x0F
                    hh_hi = (hh >> 4) & 0x0F
                    hh_lo += 1
                    if hh_lo > 9:
                        hh_lo = 0
                        hh_hi += 1
                    n_hh = (hh_hi << 4) | hh_lo
                    # interpretation: hh==0x12 -> hh=0x01
                    if n_hh == 0x13:
                        n_hh = 0x01
                    n_pm = pm

        # Output current state (before edge)
        out.append({'pm': pm, 'hh': hh, 'mm': mm, 'ss': ss})

        # Apply next state
        ss, mm, hh, pm = n_ss, n_mm, n_hh, n_pm

    return out
