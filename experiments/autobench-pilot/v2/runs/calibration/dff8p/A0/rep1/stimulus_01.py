def stimulus(rng, cycles):
    result = []
    for i in range(cycles):
        # Vary reset activity: mostly low, occasionally high
        r = rng.random()
        if r < 0.15:
            reset = 1
        else:
            reset = 0
        # Vary data: sometimes boundary values, sometimes random
        c = rng.randrange(10)
        if c == 0:
            d = 0
        elif c == 1:
            d = 0xFF
        elif c == 2:
            d = 0x34
        elif c == 3:
            d = 0x35
        elif c == 4:
            d = 0x33
        elif c == 5:
            d = 0x80
        elif c == 6:
            d = 0x7F
        else:
            d = rng.getrandbits(8)
        result.append({'d': d, 'reset': reset})
    return result
