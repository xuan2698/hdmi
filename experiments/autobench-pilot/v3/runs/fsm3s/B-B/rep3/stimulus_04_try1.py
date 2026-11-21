def fsm(in_, reset, state):
    if reset:
        return 0, 0
    if state == 0:
        return (0, 1) if in_ else (0, 0)
    if state == 1:
        return (1, 1) if in_ else (2, 0)
    if state == 2:
        return (3, 1) if in_ else (0, 0)
    return (1, 1) if in_ else (2, 1)

def stimulus(rng, cycles):
    rows = []
    rows.append({'in': 0, 'reset': 1})
    rows.append({'in': 1, 'reset': 1})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 1, 'reset': 0})
    rows.append({'in': 0, 'reset': 0})
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
        else:
            rows.append({'in': rng.getrandbits(1), 'reset': 0})
    return rows[:cycles]
