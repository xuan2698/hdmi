def reference(vectors):
    # State: BCD digits and pm. Power-up unspecified; use 12:00 AM as concrete default.
    # R1_reset: reset==1 at posedge -> 12:00 AM (hh=0x12, mm=0, ss=0, pm=0)
    # R2_hold: reset==0 && ena==0 -> hold
    # R3_seconds: ena && ss!=0x59 -> increment ss
    # R4_seconds_roll: ena && ss==0x59 && mm!=0x59 -> ss=0, mm++
    # R5_minutes_roll: ena && ss==0x59 && mm==0x59 && !(hh==0x11 && pm==0) -> ss=0,mm=0,hh++
    # R6_hours_roll_am_to_pm: ena && ss==0x59 && mm==0x59 && hh==0x11 && pm==0 -> ss=0,mm=0,hh=0x12,pm=1
    # R7_hours_roll_pm_to_am: ena && ss==0x59 && mm==0x59 && hh==0x11 && pm==1 -> ss=0,mm=0,hh=0x12,pm=0

    ss_lo = 0
    ss_hi = 0
    mm_lo = 0
    mm_hi = 0
    hh_lo = 2
    hh_hi = 1
    pm_reg = 0

    def pack(hi, lo):
        return (hi << 4) | lo

    results = []
    for row in vectors:
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)

        # Sample current outputs (before edge)
        results.append({
            'pm': pm_reg,
            'hh': pack(hh_hi, hh_lo),
            'mm': pack(mm_hi, mm_lo),
            'ss': pack(ss_hi, ss_lo),
        })

        # Compute next state at posedge
        if reset == 1:
            # R1_reset
            ss_lo = 0; ss_hi = 0
            mm_lo = 0; mm_hi = 0
            hh_lo = 2; hh_hi = 1
            pm_reg = 0
        elif ena == 0:
            # R2_hold
            pass
        else:
            ss = pack(ss_hi, ss_lo)
            mm = pack(mm_hi, mm_lo)
            hh = pack(hh_hi, hh_lo)
            if ss != 0x59:
                # R3_seconds
                if ss_lo == 9:
                    ss_lo = 0
                    ss_hi += 1
                else:
                    ss_lo += 1
            elif mm != 0x59:
                # R4_seconds_roll
                ss_lo = 0; ss_hi = 0
                if mm_lo == 9:
                    mm_lo = 0
                    mm_hi += 1
                else:
                    mm_lo += 1
            elif hh == 0x11 and pm_reg == 0:
                # R6_hours_roll_am_to_pm
                ss_lo = 0; ss_hi = 0
                mm_lo = 0; mm_hi = 0
                hh_lo = 2; hh_hi = 1
                pm_reg = 1
            elif hh == 0x11 and pm_reg == 1:
                # R7_hours_roll_pm_to_am
                ss_lo = 0; ss_hi = 0
                mm_lo = 0; mm_hi = 0
                hh_lo = 2; hh_hi = 1
                pm_reg = 0
            else:
                # R5_minutes_roll
                ss_lo = 0; ss_hi = 0
                mm_lo = 0; mm_hi = 0
                if hh_lo == 9:
                    hh_lo = 0
                    hh_hi += 1
                else:
                    hh_lo += 1

    return results
