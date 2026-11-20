def stimulus(rng, cycles):
    seq = [
        (1, 0x00000000),
        (1, 0xFFFFFFFF),
        (0, 0xFFFFFFFF),
        (0, 0x00000000),
        (0, 0x00000000),
        (0, 0xFFFFFFFF),
        (1, 0xDEADBEEF),
        (0, 0xDEADBEEF),
        (0, 0xFFFFFFFF),
        (0, 0x00000000),
        (0, 0xAAAAAAAA),
        (0, 0x55555555),
        (0, 0xFFFFFFFF),
        (0, 0x0000000F),
        (0, 0x00000000),
        (0, 0xFFFFFFF0),
        (1, 0x00000001),
        (0, 0x00000001),
        (0, 0x00000000),
        (0, 0x80000000),
        (0, 0x7FFFFFFF),
        (0, 0x00000000),
        (0, 0xFFFFFFFF),
        (0, 0x00000000),
        (1, 0xFFFFFFFF),
        (0, 0xFFFFFFFF),
        (0, 0x00000000),
    ]
    result = []
    for i in range(cycles):
        if i < len(seq):
            r, v = seq[i]
        else:
            c = rng.randrange(6)
            if c == 0:
                r = 1
                v = rng.getrandbits(32)
            elif c == 1:
                r = 0
                v = 0xFFFFFFFF
            elif c == 2:
                r = 0
                v = 0x00000000
            elif c == 3:
                r = 0
                v = rng.getrandbits(1) * 0xFFFFFFFF
            elif c == 4:
                r = 0
                v = rng.getrandbits(32)
            else:
                r = 0
                v = rng.getrandbits(32) ^ rng.getrandbits(32)
        result.append({"reset": r, "in": v})
    return result
