def stimulus(rng, cycles):
    seq = []

    for _ in range(rng.randrange(1, 4)):
        seq.append((1, 0))

    while len(seq) < cycles:
        choice = rng.randrange(10)
        if choice == 0:
            for _ in range(rng.randrange(1, 3)):
                if len(seq) < cycles:
                    seq.append((1, rng.getrandbits(1)))
        elif choice == 1:
            for _ in range(rng.randrange(2, 8)):
                if len(seq) < cycles:
                    seq.append((0, 0))
        elif choice == 2:
            for _ in range(rng.randrange(2, 8)):
                if len(seq) < cycles:
                    seq.append((0, 1))
        elif choice == 3:
            start = rng.getrandbits(1)
            for i in range(rng.randrange(2, 8)):
                if len(seq) < cycles:
                    seq.append((0, (start + i) & 1))
        elif choice == 4:
            if len(seq) < cycles:
                seq.append((0, 1))
            for _ in range(rng.randrange(2, 6)):
                if len(seq) < cycles:
                    seq.append((0, 0))
        elif choice == 5:
            for _ in range(rng.randrange(1, 5)):
                if len(seq) < cycles:
                    seq.append((0, 0))
            if len(seq) < cycles:
                seq.append((0, 1))
        else:
            for _ in range(rng.randrange(1, 6)):
                if len(seq) < cycles:
                    seq.append((0, rng.getrandbits(1)))

    seq = seq[:cycles]

    result = []
    for areset, x in seq:
        result.append({'areset': areset, 'x': x})

    return result
