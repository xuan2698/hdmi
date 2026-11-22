def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # hh is BCD 12-hour: 0x12 = 12 o'clock, 0x01 = 1 o'clock
    # Initial state (power-up unspecified, but examples imply starting at 12:00:00 AM)
    ss_ones = 0
    ss_tens = 0
    mm_ones = 0
    mm_tens = 0
    hh_ones = 2
    hh_tens = 1
    pm_state = 0

    results = []
    for v in vectors:
        reset = v.get("reset", 0)
        ena = v.get("ena", 0)

        # R1_reset: synchronous reset to 12:00 AM, priority over ena
        if reset == 1:
            ss_ones = 0
            ss_tens = 0
            mm_ones = 0
            mm_tens = 0
            hh_ones = 2
            hh_tens = 1
            pm_state = 0
        elif ena == 1:
            # R2_seconds / R3_seconds_rollover / R4_minutes_rollover / R5_hour_rollover_am_pm
            if ss_ones == 9:
                ss_ones = 0
                if ss_tens == 5:
                    ss_tens = 0
                    # seconds rolled over to 00, increment minutes
                    if mm_ones == 9:
                        mm_ones = 0
                        if mm_tens == 5:
                            mm_tens = 0
                            # minutes rolled over to 00, increment hours
                            # hh is BCD 12-hour: 0x12 (12), 0x01..0x09, 0x10, 0x11
                            if hh_tens == 1 and hh_ones == 2:
                                # 12 -> 1
                                hh_tens = 0
                                hh_ones = 1
                            elif hh_tens == 1 and hh_ones == 1:
                                # 11 -> 12, toggle pm
                                hh_ones = 2
                                pm_state = 1 - pm_state
                            elif hh_tens == 0 and hh_ones == 9:
                                # 9 -> 10
                                hh_tens = 1
                                hh_ones = 0
                            else:
                                hh_ones += 1
                        else:
                            mm_tens += 1
                    else:
                        mm_ones += 1
                else:
                    ss_tens += 1
            else:
                ss_ones += 1
        # R6_hold: ena==0 and reset==0 -> no change

        hh = (hh_tens << 4) | hh_ones
        mm = (mm_tens << 4) | mm_ones
        ss = (ss_tens << 4) | ss_ones

        results.append({"pm": pm_state, "hh": hh, "mm": mm, "ss": ss})

    return results
