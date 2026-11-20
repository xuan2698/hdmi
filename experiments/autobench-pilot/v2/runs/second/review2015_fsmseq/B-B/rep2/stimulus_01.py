def stimulus(rng, cycles):
    out = []
    state = 0
    found = False
    for i in range(cycles):
        reset = 0
        data = 0
        if i == 0:
            reset = 1
            data = rng.getrandbits(1)
        elif i == 1:
            reset = 0
            data = 1
        elif i == 2:
            data = 1
        elif i == 3:
            data = 0
        elif i == 4:
            data = 1
        elif i == 5:
            data = rng.getrandbits(1)
        elif i == 6:
            reset = 1
            data = rng.getrandbits(1)
        elif i == 7:
            reset = 0
            data = 1
        elif i == 8:
            data = 1
        elif i == 9:
            data = 0
        elif i == 10:
            data = 1
        elif i == 11:
            data = 1
        elif i == 12:
            data = 1
        elif i == 13:
            data = 0
        elif i == 14:
            data = 1
        elif i == 15:
            reset = 1
            data = 0
        elif i == 16:
            reset = 0
            data = 1
        elif i == 17:
            data = 1
        elif i == 18:
            data = 0
        elif i == 19:
            data = 1
        else:
            r = rng.random()
            if r < 0.05:
                reset = 1
                data = rng.getrandbits(1)
            elif r < 0.15:
                reset = 0
                data = 1
            elif r < 0.25:
                reset = 0
                data = 0
            else:
                reset = 0
                data = rng.getrandbits(1)
        out.append({'reset': reset, 'data': data})
    return out
