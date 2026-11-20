def stimulus(rng, cycles):
    seq = []
    for i in range(cycles):
        a = rng.getrandbits(1)
        b = rng.getrandbits(1)
        if i % 7 == 0:
            a, b = 0, 0
        elif i % 7 == 1:
            a, b = 0, 1
        elif i % 7 == 2:
            a, b = 1, 0
        elif i % 7 == 3:
            a, b = 1, 1
        elif i % 7 == 4:
            a, b = rng.choice([(0, 0), (1, 1)])
        elif i % 7 == 5:
            a, b = rng.choice([(0, 1), (1, 0)])
        seq.append({'a': a, 'b': b})
    return seq
