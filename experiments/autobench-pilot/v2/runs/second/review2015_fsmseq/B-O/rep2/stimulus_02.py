def stimulus(rng, cycles):
    seq = []
    patterns = [
        [1,1,0,1],
        [1,1,1,0,1],
        [1,0,1,1,0,1],
        [1,1,0,0,1,1,0,1],
        [0,1,1,0,1],
        [1,1,0,1,1,1,0,1],
        [1,1,1,1,0,1],
        [0,0,0,0],
        [1,1,1,1],
        [1,0,1,0,1,1,0,1],
    ]
    i = 0
    while len(seq) < cycles:
        if rng.random() < 0.15:
            seq.append({'reset': 1, 'data': rng.getrandbits(1)})
        elif rng.random() < 0.5:
            p = patterns[rng.randrange(len(patterns))]
            for b in p:
                if len(seq) >= cycles:
                    break
                seq.append({'reset': 0, 'data': b})
        else:
            n = rng.randrange(1, 8)
            for _ in range(n):
                if len(seq) >= cycles:
                    break
                seq.append({'reset': 0, 'data': rng.getrandbits(1)})
    return seq[:cycles]
