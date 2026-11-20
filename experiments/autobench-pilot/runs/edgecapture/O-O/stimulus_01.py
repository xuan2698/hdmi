def stimulus(rng, cycles):
    seq = []
    seq.append((1, 0))
    seq.append((1, 0xFFFFFFFF))
    seq.append((0, 0))
    seq.append((0, 0xFFFFFFFF))
    seq.append((0, 0))
    seq.append((0, 0xAAAAAAAA))
    seq.append((0, 0x55555555))
    seq.append((0, 0xAAAAAAAA))
    seq.append((0, 0xFFFFFFFF))
    seq.append((0, 0))
    for i in range(32):
        seq.append((0, 1 << i))
        seq.append((0, 0))
    seq.append((1, 0xFFFFFFFF))
    seq.append((1, 0))
    seq.append((0, 0xFFFFFFFF))
    seq.append((0, 0))
    seq.append((1, 0))
    seq.append((0, 0xFFFFFFFF))
    seq.append((0, 0x00000000))
    while len(seq) < cycles:
        v = rng.getrandbits(32)
        seq.append((0, v))
        if len(seq) < cycles:
            seq.append((0, v ^ 0xFFFFFFFF))
        if len(seq) < cycles:
            seq.append((0, 0))
    return [{"reset": r, "in": v} for r, v in seq[:cycles]]
