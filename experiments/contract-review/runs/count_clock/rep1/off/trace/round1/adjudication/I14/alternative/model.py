def reference(vectors):
    # State: BCD digits. Reset value: 12:00 AM -> hh=0x12, mm=0x00, ss=0x00, pm=0
    # R1_reset: reset==1 -> next state = 12:00 AM (hh=0x12, mm=0, ss=0, pm=0)
    # R2_hold: reset==0 && ena==0 -> hold
    # R3_seconds: ena && ss != 0x59 -> ss += 1 (BCD)
    # R4_seconds_roll: ena && ss==0x59 && mm!=0x59 -> ss=0, mm+=1 (BCD)
    # R5_minutes_roll: ena && ss==0x59 && mm==0x59 && !(hh==0x11 && pm==0) -> ss=0,mm=0,hh+=1 (BCD, 12->01)
    # R6_hours_roll_am_to_pm: ena && ss==0x59 && mm==0x59 && hh==0x11 && pm==0 -> ss=0,mm=0,hh=0x12,pm=1
    # R7_hours_roll_pm_to_am: ena && ss==0x59 && mm==0x59 && hh==0x11 && pm==1 -> ss=0,mm=0,hh=0x12,pm=0

    def bcd_inc(v):
        lo = v & 0xF
        hi = (v >> 4) & 0xF
        lo += 1
        if lo > 9:
            lo = 0
            hi += 1
        return ((hi & 0xF) << 4) | (lo & 0xF)

    def bcd_inc_hours(v):
        # hours 01..12 -> 0x01..0x12
        lo = v & 0xF
        hi = (v >> 4) & 0xF
        if v == 0x12:
            return 0x01
        lo += 1
        if lo > 9:
            lo = 0
            hi += 1
        return ((hi & 0xF) << 4) | (lo & 0xF)

    # initial state (power-up unspecified but we must output concrete; use reset value)
    hh = 0x12
    mm = 0x00
    ss = 0x00
    pm = 0

    results = []
    for row in vectors:
        # sample inputs at posedge (values driven before edge)
        reset = row.get('reset', 0) & 1
        ena = row.get('ena', 0) & 1

        # compute next state
        if reset:  # R1_reset
            nhh, nmm, nss, npm = 0x12, 0x00, 0x00, 0
        elif not ena:  # R2_hold
            nhh, nmm, nss, npm = hh, mm, ss, pm
        else:
            # ena == 1
            if ss != 0x59:  # R3_seconds
                nss = bcd_inc(ss)
                nmm, nhh, npm = mm, hh, pm
            elif mm != 0x59:  # R4_seconds_roll
                nss = 0x00
                nmm = bcd_inc(mm)
                nhh, npm = hh, pm
            else:
                # ss==0x59 && mm==0x59
                if hh == 0x11 and pm == 0:  # R6_hours_roll_am_to_pm
                    nss, nmm, nhh, npm = 0x00, 0x00, 0x12, 1
                elif hh == 0x11 and pm == 1:  # R7_hours_roll_pm_to_am
                    nss, nmm, nhh, npm = 0x00, 0x00, 0x12, 0
                else:  # R5_minutes_roll
                    nss, nmm = 0x00, 0x00
                    nhh = bcd_inc_hours(hh)
                    npm = pm

        hh, mm, ss, pm = nhh, nmm, nss, npm

        results.append({
            'pm': pm & 1,
            'hh': hh & 0xFF,
            'mm': mm & 0xFF,
            'ss': ss & 0xFF,
        })

    return results
