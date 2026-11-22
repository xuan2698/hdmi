def reference(vectors):
    # State: hh, mm, ss are BCD-encoded ints; pm is 0/1
    hh = 0x12
    mm = 0x00
    ss = 0x00
    pm = 0

    def bcd_inc(v):
        lo = v & 0x0F
        hi = (v >> 4) & 0x0F
        lo += 1
        if lo > 9:
            lo = 0
            hi += 1
        return (hi << 4) | lo

    out = []
    for row in vectors:
        # Sample inputs (values driven before sampled edge)
        reset = row.get('reset', 0) & 1
        ena = row.get('ena', 0) & 1

        # Compute next state (synchronous, reset has priority)
        if reset:
            nhh, nmm, nss, npm = 0x12, 0x00, 0x00, 0
        elif ena:
            nss = bcd_inc(ss)
            nmm = mm
            nhh = hh
            npm = pm
            if nss > 0x59:
                nss = 0x00
                nmm = bcd_inc(mm)
                if nmm > 0x59:
                    nmm = 0x00
                    # increment hours 01..12
                    if hh == 0x12:
                        nhh = 0x01
                        npm = pm ^ 1
                    elif hh == 0x11:
                        nhh = 0x12
                        npm = pm ^ 1
                    else:
                        nhh = bcd_inc(hh)
        else:
            nhh, nmm, nss, npm = hh, mm, ss, pm

        # Outputs reflect state after edge (one-cycle latency)
        out.append({
            'pm': npm & 1,
            'hh': nhh & 0xFF,
            'mm': nmm & 0xFF,
            'ss': nss & 0xFF,
        })

        # Update state
        hh, mm, ss, pm = nhh, nmm, nss, npm

    return out
