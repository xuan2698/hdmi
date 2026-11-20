def stimulus(rng, cycles):
    out = []
    i = 0
    while i < cycles:
        if i == 0:
            out.append({'areset': 1, 'x': 0})
            i += 1
            continue
        if rng.random() < 0.08:
            out.append({'areset': 1, 'x': rng.getrandbits(1)})
            i += 1
            continue
        if rng.random() < 0.15:
            n = rng.randrange(1, 9)
            for _ in range(n):
                if i >= cycles:
                    break
                out.append({'areset': 0, 'x': rng.getrandbits(1)})
                i += 1
            continue
        if rng.random() < 0.2:
            n = rng.randrange(1, 7)
            for _ in range(n):
                if i >= cycles:
                    break
                out.append({'areset': 0, 'x': 0})
                i += 1
            continue
        if rng.random() < 0.2:
            n = rng.randrange(1, 7)
            for _ in range(n):
                if i >= cycles:
                    break
                out.append({'areset': 0, 'x': 1})
                i += 1
            continue
        out.append({'areset': 0, 'x': rng.getrandbits(1)})
        i += 1
    return out[:cycles]
