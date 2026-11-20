def stimulus(rng, cycles):
    out = []
    i = 0
    while i < cycles:
        if i == 0 or rng.random() < 0.08:
            out.append({'areset': 1, 'x': rng.getrandbits(1)})
            i += 1
            if i < cycles:
                out.append({'areset': 0, 'x': rng.getrandbits(1)})
                i += 1
        else:
            out.append({'areset': 0, 'x': rng.getrandbits(1)})
            i += 1
    return out[:cycles]
