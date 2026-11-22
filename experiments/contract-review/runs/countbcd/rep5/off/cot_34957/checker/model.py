def reference(vectors):
    # State: 16-bit BCD counter, starts at 0 (power-up unspecified but we pick 0)
    q = 0
    out = []
    for row in vectors:
        # Pre-edge values drive combinational outputs
        reset = row.get('reset', 0) & 1
        # ena is combinational from pre-edge q, independent of reset
        d0 = q & 0xF
        d1 = (q >> 4) & 0xF
        d2 = (q >> 8) & 0xF
        d3 = (q >> 12) & 0xF
        ena = 0
        if d0 == 9:
            ena |= 1
        if d0 == 9 and d1 == 9:
            ena |= 2
        if d0 == 9 and d1 == 9 and d2 == 9:
            ena |= 4
        out.append({'q': q, 'ena': ena})
        # Compute next state from pre-edge q with reset priority
        if reset:
            q = 0
        else:
            d0 = q & 0xF
            d1 = (q >> 4) & 0xF
            d2 = (q >> 8) & 0xF
            d3 = (q >> 12) & 0xF
            d0 += 1
            if d0 == 10:
                d0 = 0
                d1 += 1
                if d1 == 10:
                    d1 = 0
                    d2 += 1
                    if d2 == 10:
                        d2 = 0
                        d3 += 1
                        if d3 == 10:
                            d3 = 0
            q = d0 | (d1 << 4) | (d2 << 8) | (d3 << 12)
    return out
