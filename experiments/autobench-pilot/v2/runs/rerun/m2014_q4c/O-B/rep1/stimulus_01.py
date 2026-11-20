def stimulus(rng, cycles):
    result = []
    for i in range(cycles):
        d = rng.getrandbits(1)
        r = 0
        if i == 0:
            r = 1
        elif i % 7 == 0:
            r = 1
        elif i % 11 == 0:
            r = rng.getrandbits(1)
        elif i % 5 == 0:
            d = 0
        elif i % 3 == 0:
            d = 1
        result.append({'d': d, 'r': r})
    return result
