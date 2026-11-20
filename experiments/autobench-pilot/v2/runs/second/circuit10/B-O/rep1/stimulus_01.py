def stimulus(rng, cycles):
    seq = []
    for i in range(cycles):
        if i % 8 == 0:
            a = rng.getrandbits(1)
            b = rng.getrandbits(1)
        elif i % 8 == 1:
            a = 0
            b = 0
        elif i % 8 == 2:
            a = 1
            b = 1
        elif i % 8 == 3:
            a = rng.choice([0, 1])
            b = 1 - a
        elif i % 8 == 4:
            a = 1
            b = 0
        elif i % 8 == 5:
            a = 0
            b = 1
        elif i % 8 == 6:
            a = rng.getrandbits(1)
            b = rng.getrandbits(1)
        else:
            a = rng.randrange(2)
            b = rng.randrange(2)
        seq.append({'a': a, 'b': b})
    return seq
