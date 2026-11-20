def stimulus(rng, cycles):
    seq = []
    i = 0
    while i < cycles:
        if i == 0 or rng.random() < 0.15:
            seq.append({'areset': 1, 'x': rng.getrandbits(1)})
            i += 1
            if i < cycles:
                seq.append({'areset': 0, 'x': rng.getrandbits(1)})
                i += 1
        else:
            seq.append({'areset': 0, 'x': rng.getrandbits(1)})
            i += 1
    return seq[:cycles]
