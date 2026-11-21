def stimulus(rng, cycles):
    rows = []
    rows.append({'in': 0, 'reset': 1})
    rows.append({'in': 1, 'reset': 1})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0, 'mid': {'in': 0}})
    rows.append({'in': 0, 'reset': 0, 'mid': {'in': 1}})
    rows.append({'in': 1, 'reset': 0, 'mid': {'reset': 1}})
    rows.append({'in': 0, 'reset': 1, 'mid': {'reset': 0}})
    rows.append({'in': 1, 'reset': 1, 'mid': {'in': 0}})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    while len(rows) < cycles:
        r = rng.randrange(4)
        if r == 0:
            rows.append({'in': rng.getrandbits(1), 'reset': 1})
        elif r == 1:
            rows.append({'in': rng.getrandbits(1), 'reset': 0, 'mid': {'in': rng.getrandbits(1)}})
        elif r == 2:
            rows.append({'in': rng.getrandbits(1), 'reset': 0, 'mid': {'reset': rng.getrandbits(1)}})
        else:
            rows.append({'in': rng.getrandbits(1), 'reset': 0})
    return rows[:cycles]
