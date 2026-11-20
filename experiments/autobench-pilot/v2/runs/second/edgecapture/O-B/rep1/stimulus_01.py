def stimulus(rng, cycles):
    result = []
    prev = 0
    for i in range(cycles):
        if i == 0:
            reset = 1
            inval = rng.getrandbits(32)
        elif i == 1:
            reset = 0
            inval = rng.getrandbits(32)
        else:
            r = rng.random()
            if r < 0.05:
                reset = 1
                inval = rng.getrandbits(32)
            elif r < 0.10:
                reset = 0
                inval = 0
            elif r < 0.15:
                reset = 0
                inval = 0xFFFFFFFF
            elif r < 0.25:
                reset = 0
                inval = prev
            elif r < 0.40:
                reset = 0
                inval = prev & rng.getrandbits(32)
            elif r < 0.55:
                reset = 0
                inval = prev | rng.getrandbits(32)
            elif r < 0.70:
                reset = 0
                inval = prev ^ rng.getrandbits(32)
            elif r < 0.85:
                reset = 0
                inval = (~prev) & 0xFFFFFFFF
            else:
                reset = 0
                inval = rng.getrandbits(32)
        prev = inval
        result.append({'reset': reset, 'in': inval})
    return result
