def stimulus(rng, cycles):
    result = []
    for i in range(cycles):
        a = rng.getrandbits(1)
        b = rng.getrandbits(1)
        result.append({'a': a, 'b': b})
    return result
