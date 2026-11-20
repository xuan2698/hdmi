def stimulus(rng, cycles):
    target = [
        (0, 1), (1, 1), (1, 0), (1, 0), (0, 0), (0, 0), (1, 0), (0, 1),
        (1, 0), (1, 1), (0, 1), (1, 0), (0, 0), (1, 0), (1, 0), (0, 0),
        (1, 0), (0, 1), (1, 0), (0, 0), (1, 0), (1, 1), (0, 0), (0, 1)
    ]
    out = []
    n = len(target)
    for i in range(cycles):
        if i < n:
            d, r = target[i]
        else:
            k = i % 10
            if k == 0:
                d = rng.getrandbits(1)
                r = 1
            elif k == 1:
                d = 1
                r = 0
            elif k == 2:
                d = 0
                r = 0
            elif k == 3:
                d = rng.getrandbits(1)
                r = 0
            elif k == 4:
                d = 1
                r = 1 if rng.getrandbits(2) == 0 else 0
            elif k == 5:
                d = rng.getrandbits(1)
                r = 1 if rng.getrandbits(2) == 0 else 0
            elif k == 6:
                d = rng.getrandbits(1)
                r = 0
            elif k == 7:
                d = 0
                r = 1
            elif k == 8:
                d = rng.getrandbits(1)
                r = 0
            else:
                d = 1
                r = 0
        out.append({"d": int(d), "r": int(r)})
    return out
