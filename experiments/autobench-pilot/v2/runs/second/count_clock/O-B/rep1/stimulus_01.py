def stimulus(rng, cycles):
    out = []
    ss = 0
    mm = 0
    hh = 12
    pm = 0
    for i in range(cycles):
        r = rng.random()
        if r < 0.05:
            reset = 1
            ena = rng.getrandbits(1)
        else:
            reset = 0
            if r < 0.15:
                ena = 0
            else:
                ena = 1
        out.append({'reset': reset, 'ena': ena})
        if reset:
            ss = 0
            mm = 0
            hh = 12
            pm = 0
        elif ena:
            ss += 1
            if ss == 60:
                ss = 0
                mm += 1
                if mm == 60:
                    mm = 0
                    hh += 1
                    if hh == 13:
                        hh = 1
                    if hh == 12:
                        pm ^= 1
    return out
