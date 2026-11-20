def stimulus(rng, cycles):
    out = []
    i = 0
    while len(out) < cycles:
        r = rng.random()
        if r < 0.08:
            n = rng.randrange(1, 4)
            for _ in range(n):
                if len(out) >= cycles:
                    break
                out.append({'areset': 1, 'x': rng.getrandbits(1)})
        elif r < 0.15:
            if len(out) >= cycles:
                break
            out.append({'areset': 1, 'x': 0})
        else:
            if len(out) >= cycles:
                break
            out.append({'areset': 0, 'x': rng.getrandbits(1)})
    return out[:cycles]
