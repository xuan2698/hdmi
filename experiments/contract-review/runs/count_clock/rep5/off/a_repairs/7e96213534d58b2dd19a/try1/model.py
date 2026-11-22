def reference(vectors):
    # Contract rules implemented:
    # R1_reset: synchronous active-high reset -> 12:00 AM (hh=0x12, mm=0x00, ss=0x00, pm=0)
    # R2_seconds: increment ss when ena and not reset and ss != 0x59
    # R3_seconds_rollover: ss 0x59 -> 0x00, increment mm (if mm != 0x59)
    # R4_minutes_rollover: mm 0x59 -> 0x00, increment hh (12-hour BCD)
    # R5_hour_rollover_am_pm: 11:59:59 -> 12:00:00 with pm toggle
    # R6_hold: when ena==0 and not reset, hold all state
    # hh is BCD 12-hour: 0x12 = 12 o'clock, 0x01 = 1 o'clock

    # Named state
    ss_ones = 0
    ss_tens = 0
    mm_ones = 0
    mm_tens = 0
    hh_ones = 2
    hh_tens = 1
    pm_state = 0

    def to_bcd(tens, ones):
        return (tens << 4) | ones

    def from_bcd(v):
        return (v >> 4) & 0xF, v & 0xF

    results = []
    for row in vectors:
        reset = row.get("reset", 0)
        ena = row.get("ena", 0)

        # Sample current outputs before edge
        ss = to_bcd(ss_tens, ss_ones)
        mm = to_bcd(mm_tens, mm_ones)
        hh = to_bcd(hh_tens, hh_ones)
        results.append({"pm": pm_state, "hh": hh, "mm": mm, "ss": ss})

        # Compute next state at posedge
        if reset:
            # R1_reset
            ss_ones, ss_tens = 0, 0
            mm_ones, mm_tens = 0, 0
            hh_ones, hh_tens = 2, 1
            pm_state = 0
        elif ena:
            # R2_seconds / R3_seconds_rollover
            if ss_tens == 5 and ss_ones == 9:
                ss_ones, ss_tens = 0, 0
                # R3_seconds_rollover -> increment minutes
                if mm_tens == 5 and mm_ones == 9:
                    mm_ones, mm_tens = 0, 0
                    # R4_minutes_rollover -> increment hours
                    # hh is BCD 12-hour: 0x12, 0x01..0x11
                    if hh_tens == 1 and hh_ones == 2:
                        # 12 -> 1
                        hh_ones, hh_tens = 1, 0
                    elif hh_tens == 1 and hh_ones == 1:
                        # 11 -> 12, toggle pm (R5_hour_rollover_am_pm)
                        hh_ones, hh_tens = 2, 1
                        pm_state = 1 - pm_state
                    else:
                        # increment ones digit
                        if hh_ones == 9:
                            hh_ones = 0
                            hh_tens += 1
                        else:
                            hh_ones += 1
                else:
                    # increment minutes
                    if mm_ones == 9:
                        mm_ones = 0
                        mm_tens += 1
                    else:
                        mm_ones += 1
            else:
                # increment seconds
                if ss_ones == 9:
                    ss_ones = 0
                    ss_tens += 1
                else:
                    ss_ones += 1
        # else R6_hold: no change

    return results
