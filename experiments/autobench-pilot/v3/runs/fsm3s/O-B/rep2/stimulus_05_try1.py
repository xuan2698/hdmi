def fsm(inp, reset, state):
    if reset:
        return 0, 0
    if state == 0:
        return (0, 1) if inp else (0, 0)
    if state == 1:
        return (1, 1) if inp else (2, 0)
    if state == 2:
        return (3, 1) if inp else (0, 0)
    return (1, 1) if inp else (2, 1)

def stimulus(rng, cycles):
    rows = []
    state = 0
    seq = [
        {'in': 0, 'reset': 1},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 1, 'reset': 0},
        {'in': 0, 'reset': 0},
        {'in': 0, 'reset': 0},
    ]
    for r in seq:
        rows.append(dict(r))
    while len(rows) < cycles:
        r = {'in': rng.getrandbits(1), 'reset': 0}
        if rng.randrange(4) == 0:
            r['mid'] = {'in': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
