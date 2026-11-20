def stimulus(rng, cycles):
    out = []
    state = 0
    found = False
    for i in range(cycles):
        reset = 0
        data = 0
        if i == 0:
            reset = 1
        elif i < 4:
            reset = 0
            data = rng.getrandbits(1)
        else:
            r = rng.random()
            if r < 0.05:
                reset = 1
            elif r < 0.15:
                data = 1
            elif r < 0.25:
                data = 0
            else:
                data = rng.getrandbits(1)
        out.append({'reset': reset, 'data': data})
    return out
