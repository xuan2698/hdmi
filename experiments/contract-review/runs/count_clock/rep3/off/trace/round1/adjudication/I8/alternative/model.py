def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # BCD helpers
    def to_bcd(v):
        return ((v // 10) << 4) | (v % 10)
    def from_bcd(v):
        return (v >> 4) * 10 + (v & 0xF)

    # Initialize to 12:00 AM (hh=0x12, mm=0x00, ss=0x00, pm=0)
    ss_lo, ss_hi = 0, 0
    mm_lo, mm_hi = 0, 0
    hh_lo, hh_hi = 2, 1  # 0x12
    pm_reg = 0

    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # R1_reset: reset has priority over enable; sync reset to 12:00 AM
        if reset == 1:
            ss_lo, ss_hi = 0, 0
            mm_lo, mm_hi = 0, 0
            hh_lo, hh_hi = 2, 1
            pm_reg = 0
        elif ena == 1:
            # R2_seconds / R3_seconds_rollover / R4_minutes_rollover /
            # R5_hour_rollover_am_pm / R6_hour_rollover_1159pm
            ss = from_bcd((ss_hi << 4) | ss_lo)
            mm = from_bcd((mm_hi << 4) | mm_lo)
            hh = from_bcd((hh_hi << 4) | hh_lo)

            if ss != 59:
                # R2_seconds: increment seconds
                ss += 1
                ss_lo = ss % 10
                ss_hi = ss // 10
            else:
                # seconds rollover
                ss = 0
                ss_lo, ss_hi = 0, 0
                if mm != 59:
                    # R3_seconds_rollover: increment minutes
                    mm += 1
                    mm_lo = mm % 10
                    mm_hi = mm // 10
                else:
                    # minutes rollover
                    mm = 0
                    mm_lo, mm_hi = 0, 0
                    if not (hh == 11 and pm_reg == 1):
                        # R4_minutes_rollover: increment hours (not 11:59 PM)
                        if hh == 12:
                            hh = 1
                        else:
                            hh += 1
                        hh_lo = hh % 10
                        hh_hi = hh // 10
                    else:
                        # R5_hour_rollover_am_pm: 11:59 PM -> 12:00 AM
                        hh = 12
                        hh_lo, hh_hi = 2, 1
                        pm_reg = 0
            # R6_hour_rollover_1159pm handled implicitly: 12:59 PM -> 1:00 PM
            # (hh==12 and pm==1 with mm==59,ss==59 -> hh becomes 1, pm stays 1)
            # Wait: need to handle 12:59 PM -> 1:00 PM correctly.
            # The above R4 branch: hh==12 -> hh=1, pm unchanged (stays 1). Correct.
            # And 11:59 AM -> 12:00 PM: hh==11, pm==0 -> hh=12, pm stays 0. Correct.
            # And 11:59 PM -> 12:00 AM: handled by R5. Correct.
        # else: R7_hold: ena==0, no change

        out.append({
            'pm': pm_reg,
            'hh': (hh_hi << 4) | hh_lo,
            'mm': (mm_hi << 4) | mm_lo,
            'ss': (ss_hi << 4) | ss_lo,
        })
    return out
