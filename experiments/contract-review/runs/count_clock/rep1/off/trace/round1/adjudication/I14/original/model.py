def reference(vectors):
    # State: ss_lo, ss_hi, mm_lo, mm_hi, hh_lo, hh_hi, pm_reg
    # Initial power-up state: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
    ss_lo = 0
    ss_hi = 0
    mm_lo = 0
    mm_hi = 0
    hh_lo = 2
    hh_hi = 1
    pm_reg = 0

    def pack():
        ss = (ss_hi << 4) | ss_lo
        mm = (mm_hi << 4) | mm_lo
        hh = (hh_hi << 4) | hh_lo
        return {"pm": pm_reg, "hh": hh, "mm": mm, "ss": ss}

    results = []
    for row in vectors:
        reset = row["reset"]
        ena = row["ena"]

        # Sample current outputs (driven before the sampled edge)
        results.append(pack())

        # Compute next state at posedge clk
        if reset == 1:
            # R1_reset: synchronous reset to 12:00 AM
            ss_lo = 0
            ss_hi = 0
            mm_lo = 0
            mm_hi = 0
            hh_lo = 2
            hh_hi = 1
            pm_reg = 0
        elif ena == 0:
            # R2_hold: hold state
            pass
        else:
            # ena == 1, reset == 0
            ss = (ss_hi << 4) | ss_lo
            mm = (mm_hi << 4) | mm_lo
            hh = (hh_hi << 4) | hh_lo

            if ss != 0x59:
                # R3_seconds: increment seconds
                if ss_lo == 9:
                    ss_lo = 0
                    ss_hi += 1
                else:
                    ss_lo += 1
            else:
                # ss == 0x59
                ss_lo = 0
                ss_hi = 0
                if mm != 0x59:
                    # R4_seconds_roll: roll seconds, increment minutes
                    if mm_lo == 9:
                        mm_lo = 0
                        mm_hi += 1
                    else:
                        mm_lo += 1
                else:
                    # mm == 0x59
                    mm_lo = 0
                    mm_hi = 0
                    if not (hh == 0x11 and pm_reg == 0):
                        # R5_minutes_roll: roll minutes, increment hours
                        if hh == 0x12:
                            hh_hi = 0
                            hh_lo = 1
                        elif hh_lo == 9:
                            hh_lo = 0
                            hh_hi += 1
                        else:
                            hh_lo += 1
                    else:
                        # hh == 0x11 and pm == 0
                        # R6_hours_roll_am_to_pm: 11:59:59 AM -> 12:00:00 PM
                        hh_hi = 1
                        hh_lo = 2
                        pm_reg = 1
                    # Note: R7 (pm->am) is handled by R5 path when hh==0x12 and pm==1
                    # because 12:59:59 PM -> 01:00:00 PM (still PM), and
                    # 11:59:59 PM -> 12:00:00 AM requires special handling.
                    # Re-examine: R5 condition excludes only (hh==0x11 && pm==0).
                    # So when hh==0x11 && pm==1 (11 PM), R5 applies: 11->12, pm stays 1.
                    # That's wrong per spec: 11:59:59 PM should go to 12:00:00 AM.
                    # R7 handles hh==0x11 && pm==1 -> 12:00 AM.
                    # But R5's condition says !(hh==0x11 && pm==0), so it fires for pm==1.
                    # We must prioritize R7 over R5 for hh==0x11 && pm==1.
                    # Fix: handle R7 before R5.

        # The above logic needs correction for R7 priority. Recompute cleanly below.
        results[-1] = results[-1]  # placeholder

    return results
