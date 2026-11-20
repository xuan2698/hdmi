def stimulus(rng, cycles):
    result = []
    seq = []

    reset_len = rng.randrange(1, 4)
    for _ in range(reset_len):
        seq.append((0, rng.getrandbits(1), rng.getrandbits(1)))

    num_rounds = rng.randrange(1, 4)
    for r in range(num_rounds):
        seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))
        seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))

        noise_len = rng.randrange(0, 3)
        for _ in range(noise_len):
            seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))

        seq.append((1, 1, rng.getrandbits(1)))
        seq.append((1, 0, rng.getrandbits(1)))
        seq.append((1, 1, rng.getrandbits(1)))

        outcome = rng.randrange(0, 3)
        if outcome == 0:
            seq.append((1, rng.getrandbits(1), 1))
            for _ in range(rng.randrange(1, 4)):
                seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))
        elif outcome == 1:
            seq.append((1, rng.getrandbits(1), 0))
            seq.append((1, rng.getrandbits(1), 1))
            for _ in range(rng.randrange(1, 4)):
                seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))
        else:
            seq.append((1, rng.getrandbits(1), 0))
            seq.append((1, rng.getrandbits(1), 0))
            for _ in range(rng.randrange(1, 4)):
                seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))

        if r < num_rounds - 1:
            for _ in range(rng.randrange(1, 3)):
                seq.append((0, rng.getrandbits(1), rng.getrandbits(1)))

    while len(seq) < cycles:
        if rng.random() < 0.1:
            seq.append((0, rng.getrandbits(1), rng.getrandbits(1)))
        else:
            seq.append((1, rng.getrandbits(1), rng.getrandbits(1)))

    seq = seq[:cycles]

    for (rv, xv, yv) in seq:
        result.append({'resetn': rv, 'x': xv, 'y': yv})

    return result
