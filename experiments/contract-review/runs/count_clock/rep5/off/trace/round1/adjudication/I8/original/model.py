def reference(vectors):
    # State: ss_ones, ss_tens, mm_ones, mm_tens, hh_ones, hh_tens, pm_state
    # Initial (power-up) state: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
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

        # R1_reset: synchronous reset to 12:00 AM, highest priority
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
                    # seconds rolled over -> increment minutes
                    if mm_ones == 9:
                        mm_ones = 0
                        if mm_tens == 5:
                            mm_tens = 0
                            # minutes rolled over -> increment hours
                            if hh_tens == 1 and hh_ones == 2:
                                # 12 -> 1, toggle pm
                                hh_tens = 0
                                hh_ones = 1
                                pm_state = 1 - pm_state
                            elif hh_ones == 9:
                                hh_ones = 0
                                hh_tens = 1
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

        results.append(pack())

    return results
