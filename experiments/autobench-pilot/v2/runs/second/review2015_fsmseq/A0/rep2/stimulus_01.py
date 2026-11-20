def stimulus(rng, cycles):
    out = []
    state = 0
    found = False
    seq = [1, 1, 0, 1]
    idx = 0
    for i in range(cycles):
        reset = 0
        data = 0
        if i == 0:
            reset = 1
        elif rng.random() < 0.05:
            reset = 1
        else:
            if rng.random() < 0.6:
                data = seq[idx]
                idx = (idx + 1) % 4
            else:
                data = rng.getrandbits(1)
        out.append({'reset': reset, 'data': data})
    return out
