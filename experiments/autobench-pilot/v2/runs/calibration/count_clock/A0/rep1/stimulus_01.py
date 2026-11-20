def stimulus(rng, cycles):
    result = []
    # Start with reset to establish known state
    for i in range(cycles):
        d = {}
        # Reset occasionally, especially at start and randomly
        if i == 0:
            d['reset'] = 1
            d['ena'] = 0
        elif i == 1:
            d['reset'] = 0
            d['ena'] = 1
        else:
            r = rng.random()
            if r < 0.03:
                d['reset'] = 1
                d['ena'] = rng.getrandbits(1)
            else:
                d['reset'] = 0
                # Enable mostly on to exercise counting
                if r < 0.15:
                    d['ena'] = 0
                else:
                    d['ena'] = 1
        result.append(d)
    return result
