def stimulus(rng, cycles):
    result = []
    for i in range(cycles):
        d = rng.getrandbits(8)
        reset = 0
        if i == 0:
            reset = 1
        elif i < 4:
            reset = rng.choice([0, 1])
        elif i % 7 == 0:
            reset = 1
        elif i % 5 == 0:
            d = rng.choice([0, 255, 1, 128, 127])
        result.append({'d': d, 'reset': reset})
    return result
