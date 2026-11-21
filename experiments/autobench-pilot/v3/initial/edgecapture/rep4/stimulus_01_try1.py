def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1, 'in': 0})
    rows.append({'reset': 1, 'in': 0xFFFFFFFF})
    rows.append({'reset': 0, 'in': 0xFFFFFFFF})
    rows.append({'reset': 0, 'in': 0xFFFFFFFF, 'mid': {'in': 0}})
    rows.append({'reset': 0, 'in': 0})
    rows.append({'reset': 0, 'in': 0xAAAAAAAA})
    rows.append({'reset': 0, 'in': 0x55555555})
    rows.append({'reset': 0, 'in': 0xAAAAAAAA, 'mid': {'in': 0x55555555}})
    rows.append({'reset': 0, 'in': 0x55555555, 'mid': {'in': 0xAAAAAAAA}})
    rows.append({'reset': 0, 'in': 0xFFFFFFFF, 'mid': {'in': 0x00000000}})
    rows.append({'reset': 0, 'in': 0x00000000, 'mid': {'in': 0xFFFFFFFF}})
    rows.append({'reset': 0, 'in': 0xF0F0F0F0})
    rows.append({'reset': 0, 'in': 0x0F0F0F0F})
    rows.append({'reset': 0, 'in': 0xFFFFFFFF, 'mid': {'in': 0xFFFFFFFE}})
    rows.append({'reset': 0, 'in': 0xFFFFFFFE, 'mid': {'in': 0xFFFFFFFF}})
    rows.append({'reset': 0, 'in': 0x80000001})
    while len(rows) < cycles:
        r = rng.randrange(0, 8)
        if r == 0:
            rows.append({'reset': 1, 'in': rng.getrandbits(32)})
        elif r == 1:
            prev = rows[-1]['in']
            rows.append({'reset': 0, 'in': prev, 'mid': {'in': rng.getrandbits(32)}})
        elif r == 2:
            rows.append({'reset': 0, 'in': 0xFFFFFFFF, 'mid': {'in': rng.getrandbits(32)}})
        elif r == 3:
            rows.append({'reset': 0, 'in': rng.getrandbits(32), 'mid': {'in': 0}})
        elif r == 4:
            rows.append({'reset': 0, 'in': 0, 'mid': {'in': rng.getrandbits(32)}})
        elif r == 5:
            rows.append({'reset': 0, 'in': rng.choice([0xFFFFFFFF, 0, 0xAAAAAAAA, 0x55555555])})
        else:
            rows.append({'reset': 0, 'in': rng.getrandbits(32)})
    return rows[:cycles]
