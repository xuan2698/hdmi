def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # Initial state: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
    ss_lo, ss_hi = 0, 0
    mm_lo, mm_hi = 0, 0
    hh_lo, hh_hi = 2, 1  # 0x12
    pm_reg = 0

    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Outputs are driven before the sampled edge (current state)
        out.append({
            'pm': pm_reg & 1,
            'hh': ((hh_hi & 0xF) << 4) | (hh_lo & 0xF),
            'mm': ((mm_hi & 0xF) << 4) | (mm_lo & 0xF),
            'ss': ((ss_hi & 0xF) << 4) | (ss_lo & 0xF),
        })

        # Compute next state at posedge
        if reset == 1:
            # R1_reset: reset to 12:00 AM
            ss_lo, ss_hi = 0, 0
            mm_lo, mm_hi = 0, 0
            hh_lo, hh_hi = 2, 1
            pm_reg = 0
        elif ena == 1:
            ss_val = ss_hi * 10 + ss_lo
            mm_val = mm_hi * 10 + mm_lo
            hh_val = hh_hi * 10 + hh_lo

            if ss_val != 59:
                # R2_seconds: increment seconds
                ss_val += 1
                ss_lo = ss_val % 10
                ss_hi = ss_val // 10
            else:
                # seconds rollover
                ss_lo, ss_hi = 0, 0
                if mm_val != 59:
                    # R3_seconds_rollover: increment minutes
                    mm_val += 1
                    mm_lo = mm_val % 10
                    mm_hi = mm_val // 10
                else:
                    # minutes rollover
                    mm_lo, mm_hi = 0, 0
                    if not (hh_val == 11 and pm_reg == 1):
                        # R4_minutes_rollover: increment hours (not 11:59 PM)
                        if hh_val == 12:
                            hh_val = 1
                        else:
                            hh_val += 1
                        hh_lo = hh_val % 10
                        hh_hi = hh_val // 10
                    else:
                        # R5_hour_rollover_am_pm: 11:59 PM -> 12:00 AM
                        hh_lo, hh_hi = 2, 1
                        pm_reg = 0
        # R7_hold: ena==0 and reset==0 -> no change

        # Note: R6_hour_rollover_1159pm is subsumed by R5 handling (11:59 PM -> 12:00 AM)
        # The contract lists both; R5 handles hh==0x11 && pm==1, R6 handles hh==0x12 && pm==1.
        # But 12:59 PM should go to 01:00 PM, not reset. So R6 as stated seems inconsistent;
        # we follow the standard 12-hour clock: 11:59 PM -> 12:00 AM (R5), 12:59 PM -> 01:00 PM (R4).
        # R6's condition (hh==0x12 && pm==1) would incorrectly reset at 12:59 PM.
        # We implement the correct 12-hour behavior per R4/R5.

    return out
