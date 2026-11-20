def stimulus(rng, cycles):
    out = []
    seq = [1, 1, 0, 1]
    i = 0
    reset_pending = True
    while len(out) < cycles:
        if reset_pending:
            out.append({'reset': 1, 'data': rng.getrandbits(1)})
            reset_pending = False
            i = 0
            continue
        if len(out) < cycles and rng.random() < 0.08:
            out.append({'reset': 1, 'data': rng.getrandbits(1)})
            i = 0
            continue
        if rng.random() < 0.5:
            bit = seq[i % 4]
            i += 1
        else:
            bit = rng.getrandbits(1)
        out.append({'reset': 0, 'data': bit})
    return out[:cycles]
