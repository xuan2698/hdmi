def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1, 'in': 0})
    rows.append({'reset': 0, 'in': 0xFFFFFFFF})
    rows.append({'reset': 0, 'in': 0xFFFFFFFF, 'mid': {'in': 0}})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 0xAAAAAAAA})
    rows.append({'reset': 0, 'in': 0x55555555})
    rows.append({'reset': 0, 'in': 0x55555555, 'mid': {'in': 0xAAAAAAAA}})
    rows.append({'reset': 0, 'in': 0xAAAAAAAA})
    rows.append({'reset': 0, 'in': 0xFFFFFFFF})
    rows.append({'reset': 0, 'in': 0xFFFFFFFF, 'mid': {'in': 0x00000000}})
    rows.append({'reset': 0, 'in': 0x00000000})
    rows.append({'reset': 1, 'in': 0xFFFFFFFF})
    rows.append({'reset': 0, 'in': 0xFFFFFFFF})
    rows.append({'reset': 0, 'in': 0x00000000})
    rows.append({'reset': 0, 'in': 0x12345678})
    rows.append({'reset': 0, 'in': 0x87654321})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'reset': 1, 'in': rng.getrandbits(32)})
        elif r == 1:
            rows.append({'reset': 0, 'in': rng.getrandbits(32)})
        elif r == 2:
            v = rng.getrandbits(32)
            rows.append({'reset': 0, 'in': v, 'mid': {'in': rng.getrandbits(32)}})
        else:
            v = rng.choice([0, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555])
            rows.append({'reset': 0, 'in': v})
    return rows[:cycles]
