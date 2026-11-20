def stimulus(rng, cycles):
    seq = []
    for i in range(cycles):
        if i % 7 == 0:
            a = rng.getrandbits(1)
            b = rng.getrandbits(1)
        elif i % 5 == 0:
            a = 1
            b = 1
        elif i % 3 == 0:
            a = 0
            b = 0
        else:
            a = rng.choice([0, 1])
            b = rng.choice([0, 1])
        seq.append({'a': a, 'b': b})
    return seq
