def stimulus(rng, cycles):
    seq = []
    for i in range(cycles):
        r = rng.randrange(8)
        if r == 0:
            a, b = 0, 0
        elif r == 1:
            a, b = 0, 1
        elif r == 2:
            a, b = 1, 0
        elif r == 3:
            a, b = 1, 1
        elif r == 4:
            a, b = rng.getrandbits(1), rng.getrandbits(1)
        elif r == 5:
            a, b = 1, 1
        elif r == 6:
            a, b = 0, 0
        else:
            a, b = rng.choice([(0,0),(0,1),(1,0),(1,1)])
        seq.append({'a': a, 'b': b})
    return seq
