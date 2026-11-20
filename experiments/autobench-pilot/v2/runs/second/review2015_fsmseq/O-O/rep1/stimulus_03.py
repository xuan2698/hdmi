def stimulus(rng, cycles):
    rows = []
    def add(reset, data):
        rows.append({'reset': reset, 'data': data})
    add(1, 0)
    add(1, 1)
    add(0, 1)
    add(0, 1)
    add(0, 0)
    add(0, 1)
    add(0, 1)
    add(0, 1)
    add(0, 0)
    add(0, 1)
    add(1, 0)
    add(0, 1)
    add(0, 1)
    add(0, 0)
    add(0, 1)
    add(0, 1)
    while len(rows) < cycles:
        r = rng.random()
        if r < 0.08:
            add(1, rng.getrandbits(1))
        else:
            add(0, rng.getrandbits(1))
    return rows[:cycles]
