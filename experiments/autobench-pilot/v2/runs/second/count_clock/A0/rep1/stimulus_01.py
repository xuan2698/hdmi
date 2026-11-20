def stimulus(rng, cycles):
    out = []
    for i in range(cycles):
        r = 1 if rng.random() < 0.05 else 0
        e = 1 if rng.random() < 0.7 else 0
        out.append({'reset': r, 'ena': e})
    return out
