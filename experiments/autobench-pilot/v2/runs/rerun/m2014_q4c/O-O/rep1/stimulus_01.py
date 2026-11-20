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
            d = 1
            r = 0
        elif i == 3:
            d = 0
            r = 0
        elif i == 4:
            d = 1
            r = 1
        elif i == 5:
            d = 0
            r = 0
        elif i == 6:
            d = 1
            r = 0
        elif i == 7:
            d = 1
            r = 0
        elif i == 8:
            d = 0
            r = 0
        elif i == 9:
            d = 0
            r = 0
        elif i == 10:
            d = 1
            r = 1
        elif i == 11:
            d = 1
            r = 0
        else:
            mode = rng.randrange(4)
            if mode == 0:
                d = rng.getrandbits(1)
                r = 0
            elif mode == 1:
                d = rng.getrandbits(1)
                r = 1
            elif mode == 2:
                d = 1
                r = rng.getrandbits(1)
            else:
                d = 0
                r = rng.getrandbits(1)
        result.append({'d': d, 'r': r})
    return result
