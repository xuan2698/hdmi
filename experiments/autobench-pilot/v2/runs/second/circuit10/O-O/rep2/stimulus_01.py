def stimulus(rng, cycles):
    seq = []
    for i in range(cycles):
        a = rng.getrandbits(1)
        b = rng.getrandbits(1)
        seq.append({'a': a, 'b': b})
    return seq
