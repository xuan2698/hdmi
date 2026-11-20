def stimulus(rng, cycles):
    out = []
    i = 0
    while len(out) < cycles:
        if i == 0:
            out.append({'areset': 1, 'x': 0})
            i += 1
            continue
        if i == 1:
            out.append({'areset': 0, 'x': rng.getrandbits(1)})
            i += 1
            continue
        r = rng.random()
        if r < 0.08:
            out.append({'areset': 1, 'x': rng.getrandbits(1)})
        elif r < 0.16:
            out.append({'areset': 0, 'x': 0})
        elif r < 0.24:
            out.append({'areset': 0, 'x': 1})
        else:
            out.append({'areset': 0, 'x': rng.getrandbits(1)})
        i += 1
    return out[:cycles]
