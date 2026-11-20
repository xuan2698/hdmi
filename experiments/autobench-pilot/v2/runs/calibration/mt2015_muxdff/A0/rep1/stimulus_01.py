def stimulus(rng, cycles):
    samples = []
    for i in range(cycles):
        L = rng.getrandbits(1)
        q_in = rng.getrandbits(1)
        r_in = rng.getrandbits(1)
        samples.append({'L': L, 'q_in': q_in, 'r_in': r_in})
    return samples
