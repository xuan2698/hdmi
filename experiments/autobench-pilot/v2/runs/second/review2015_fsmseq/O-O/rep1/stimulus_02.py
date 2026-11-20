def stimulus(rng, cycles):
    rows = []
    def add(reset, data):
        rows.append({'reset': reset, 'data': data})
    add(1, 0)
    add(0, 1)
    add(0, 1)
    add(0, 0)
    add(0, 1)
    add(0, 1)
    add(0, 1)
    add(0, 0)
    add(0, 1)
    add(1, 1)
    add(0, 0)
    add(0, 1)
    add(0, 1)
    add(0, 0)
    add(0, 1)
    add(0, 1)
    while len(rows) < cycles:
        r = 1 if rng.random() < 0.08 else 0
        d = rng.getrandbits(1)
        add(r, d)
    return rows[:cycles]
