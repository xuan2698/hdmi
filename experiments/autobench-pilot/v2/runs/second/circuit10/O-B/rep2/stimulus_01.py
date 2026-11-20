def stimulus(rng, cycles):
    seq = []
    for i in range(cycles):
        if i < 4:
            a = rng.getrandbits(1)
            b = rng.getrandbits(1)
        else:
            r = rng.random()
            if r < 0.25:
                a, b = 0, 0
            elif r < 0.5:
                a, b = 0, 1
            elif r < 0.75:
                a, b = 1, 0
            else:
                a, b = 1, 1
        seq.append({'a': a, 'b': b})
    return seq
