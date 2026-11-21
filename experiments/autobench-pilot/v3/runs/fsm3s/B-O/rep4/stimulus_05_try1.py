def stimulus(rng, cycles):
    rows = []
    rows.append({'in': 0, 'reset': 1})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
    while len(rows) < cycles:
        r = rng.randrange(100)
        if r < 5:
            rows.append({'in': rng.getrandbits(1), 'reset': 1})
        elif r < 15:
            rows.append({'in': rng.getrandbits(1), 'reset': 0,
                         'mid': {'in': rng.getrandbits(1)}})
        else:
            rows.append({'in': rng.getrandbits(1), 'reset': 0})
    return rows[:cycles]
