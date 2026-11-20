def stimulus(rng, cycles):
    seq = []
    i = 0
    while len(seq) < cycles:
        r = rng.random()
        if r < 0.15:
            n = rng.randrange(1, 4)
            for _ in range(n):
                if len(seq) >= cycles:
                    break
                seq.append({'areset': 1, 'x': rng.getrandbits(1)})
        else:
            n = rng.randrange(1, 12)
            for _ in range(n):
                if len(seq) >= cycles:
                    break
                seq.append({'areset': 0, 'x': rng.getrandbits(1)})
        i += 1
    return seq[:cycles]
