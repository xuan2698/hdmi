def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # hh is BCD 12-hour: 0x12 = 12 o'clock, 0x01 = 1 o'clock, etc.
    # Initial state (power-up unspecified, but we track it): 12:00 AM
    ss_ones = 0
    ss_tens = 0
    mm_ones = 0
    mm_tens = 0
    hh_ones = 2
    hh_tens = 1
    pm_state = 0

    def pack():
        ss = (ss_tens << 4) | ss_ones
        mm = (mm_tens << 4) | mm_ones
        hh = (hh_tens << 4) | hh_ones
        return {"pm": pm_state, "hh": hh, "mm": mm, "ss": ss}

    results = []
    for row in vectors:
        reset = row.get("reset", 0)
        ena = row.get("ena", 0)

        # Sample current outputs (before edge)
        results.append(pack())

        # Compute next state at posedge
        if reset == 1:
            # R1_reset: reset to 12:00 AM
            ss_ones = 0
            ss_tens = 0
            mm_ones = 0
            mm_tens = 0
            hh_ones = 2
            hh_tens = 1
            pm_state = 0
        elif ena == 1:
            # R2_seconds / R3_seconds_rollover / R4_minutes_rollover / R5_hour_rollover_am_pm
            ss = (ss_tens << 4) | ss_ones
            mm = (mm_tens << 4) | mm_ones
            hh = (hh_tens << 4) | hh_ones

            if ss != 0x59:
                # R2_seconds: increment seconds
                if ss_ones == 9:
                    ss_ones = 0
                    ss_tens += 1
                else:
                    ss_ones += 1
            else:
                # seconds rollover
                ss_ones = 0
                ss_tens = 0
                if mm != 0x59:
                    # R3_seconds_rollover: increment minutes
                    if mm_ones == 9:
                        mm_ones = 0
                        mm_tens += 1
                    else:
                        mm_ones += 1
                else:
                    # minutes rollover
                    mm_ones = 0
                    mm_tens = 0
                    if hh != 0x12:
                        # R4_minutes_rollover: increment hours (not 12 -> 1)
                        # hh is BCD 12-hour: 0x01..0x12
                        if hh_ones == 9:
                            hh_ones = 0
                            hh_tens += 1
                        else:
                            hh_ones += 1
                    else:
                        # R5_hour_rollover_am_pm: 12:59:59 -> 1:00:00, toggle pm
                        hh_ones = 1
                        hh_tens = 0
                        pm_state = 1 - pm_state
        # else: R6_hold: no change

    return results
