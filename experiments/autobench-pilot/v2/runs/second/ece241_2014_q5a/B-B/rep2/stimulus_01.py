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
            r = rng.random()
            if r < 0.5:
                x = 0
            elif r < 0.9:
                x = 1
            else:
                x = rng.getrandbits(1)
            out.append({'areset': 0, 'x': x})
            i += 1
    return out[:cycles]
