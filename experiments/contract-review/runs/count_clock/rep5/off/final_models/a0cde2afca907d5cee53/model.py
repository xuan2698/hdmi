def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # hh is BCD 12-hour: 0x12 = 12 o'clock, 0x01 = 1 o'clock, etc.
    # R1_reset: reset==1 -> pm=0, hh=0x12, mm=0, ss=0 (sync, priority 1)
    # R2_seconds: ena && ss!=0x59 -> ss+1
    # R3_seconds_rollover: ena && ss==0x59 && mm!=0x59 -> ss=0, mm+1
    # R4_minutes_rollover: ena && ss==0x59 && mm==0x59 && hh!=0x12 -> ss=0,mm=0,hh+1
    # R5_hour_rollover_am_pm: ena && ss==0x59 && mm==0x59 && hh==0x11 -> ss=0,mm=0,hh=0x12,pm^=1
    # R6_hold: ena==0 -> hold

    # Initialize state (power-up unspecified; use reset value as concrete)
    ss_ones = 0
    ss_tens = 0
    mm_ones = 0
    mm_tens = 0
    hh_ones = 2
    hh_tens = 1
    pm_state = 0

    results = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Compute next state based on current state and inputs (sampled at posedge)
        if reset == 1:
            # R1_reset
            n_ss_ones, n_ss_tens = 0, 0
            n_mm_ones, n_mm_tens = 0, 0
            n_hh_ones, n_hh_tens = 2, 1
            n_pm = 0
        elif ena == 1:
            ss = ss_tens * 10 + ss_ones
            mm = mm_tens * 10 + mm_ones
            hh = hh_tens * 10 + hh_ones
            if ss != 59:
                # R2_seconds
                n_ss_ones, n_ss_tens = ss_ones, ss_tens
                n_mm_ones, n_mm_tens = mm_ones, mm_tens
                n_hh_ones, n_hh_tens = hh_ones, hh_tens
                n_pm = pm_state
                # increment seconds
                if ss_ones == 9:
                    n_ss_ones = 0
                    n_ss_tens = ss_tens + 1
                else:
                    n_ss_ones = ss_ones + 1
            elif mm != 59:
                # R3_seconds_rollover
                n_ss_ones, n_ss_tens = 0, 0
                n_hh_ones, n_hh_tens = hh_ones, hh_tens
                n_pm = pm_state
                if mm_ones == 9:
                    n_mm_ones = 0
                    n_mm_tens = mm_tens + 1
                else:
                    n_mm_ones = mm_ones + 1
                    n_mm_tens = mm_tens
            elif hh != 0x12:
                # R4_minutes_rollover
                n_ss_ones, n_ss_tens = 0, 0
                n_mm_ones, n_mm_tens = 0, 0
                n_pm = pm_state
                # increment hour (BCD 12-hour: 1..12)
                if hh_ones == 9:
                    n_hh_ones = 0
                    n_hh_tens = hh_tens + 1
                else:
                    n_hh_ones = hh_ones + 1
                    n_hh_tens = hh_tens
            else:
                # hh == 0x12 (12 o'clock) -> rollover to 1, toggle pm
                # R5_hour_rollover_am_pm
                n_ss_ones, n_ss_tens = 0, 0
                n_mm_ones, n_mm_tens = 0, 0
                n_hh_ones, n_hh_tens = 1, 0
                n_pm = 1 - pm_state
        else:
            # R6_hold
            n_ss_ones, n_ss_tens = ss_ones, ss_tens
            n_mm_ones, n_mm_tens = mm_ones, mm_tens
            n_hh_ones, n_hh_tens = hh_ones, hh_tens
            n_pm = pm_state

        # Output current state (before edge)
        hh_out = (hh_tens << 4) | hh_ones
        mm_out = (mm_tens << 4) | mm_ones
        ss_out = (ss_tens << 4) | ss_ones
        results.append({
            'pm': pm_state,
            'hh': hh_out,
            'mm': mm_out,
            'ss': ss_out,
        })

        # Apply next state
        ss_ones, ss_tens = n_ss_ones, n_ss_tens
        mm_ones, mm_tens = n_mm_ones, n_mm_tens
        hh_ones, hh_tens = n_hh_ones, n_hh_tens
        pm_state = n_pm

    return results
