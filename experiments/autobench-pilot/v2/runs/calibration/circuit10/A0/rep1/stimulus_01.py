def stimulus(rng, cycles):
    seq = []
    # Targeted sequence to cover the observed behavior
    targeted = [
        (1, 0), (0, 0), (0, 0), (0, 0), (0, 0),
        (0, 1), (1, 0), (1, 1), (0, 0), (1, 1),
        (1, 1), (1, 1), (1, 0), (0, 1), (0, 0),
        (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
    ]
    for i in range(cycles):
        if i < len(targeted):
            a, b = targeted[i]
        else:
            r = rng.randrange(4)
            a = (r >> 1) & 1
            b = r & 1
        seq.append({'a': a, 'b': b})
    return seq
