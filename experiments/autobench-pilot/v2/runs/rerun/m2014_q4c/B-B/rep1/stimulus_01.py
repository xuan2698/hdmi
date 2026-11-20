def stimulus(rng, cycles):
    result = []
    for i in range(cycles):
        if i == 0:
            d = rng.getrandbits(1)
            r = 1
        elif i == 1:
            d = rng.getrandbits(1)
            r = 0
        elif i == 2:
            d = rng.getrandbits(1)
            r = 0
        elif i == 3:
            d = 1
            r = 1
        elif i == 4:
            d = 0
            r = 0
        elif i == 5:
            d = 1
            r = 0
        elif i == 6:
            d = 0
            r = 1
        elif i == 7:
            d = 1
            r = 1
        elif i == 8:
            d = 0
            r = 0
        elif i == 9:
            d = 1
            r = 0
        else:
            d = rng.getrandbits(1)
            r = 1 if rng.random() < 0.15 else 0
        result.append({'d': d, 'r': r})
    return result
