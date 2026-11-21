def stimulus(rng, cycles):
    rows = []
    rows.append({'a': 1, 'b': 0})
    rows.append({'a': 0, 'b': 1})
    rows.append({'a': 1, 'b': 1})
    rows.append({'a': 0, 'b': 0})
    rows.append({'a': 1, 'b': 0, 'mid': {'a': 0}})
    rows.append({'a': 0, 'b': 1, 'mid': {'b': 0}})
    rows.append({'a': 1, 'b': 1, 'mid': {'a': 0, 'b': 0}})
    rows.append({'a': 0, 'b': 0, 'mid': {'a': 1, 'b': 1}})
    rows.append({'a': 1, 'b': 0, 'mid': {'b': 1}})
    rows.append({'a': 0, 'b': 1, 'mid': {'a': 1}})
    rows.append({'a': 1, 'b': 1, 'mid': {'a': 0}})
    rows.append({'a': 0, 'b': 0, 'mid': {'b': 1}})
    while len(rows) < cycles:
        r = rng.randrange(4)
        a = (r >> 1) & 1
        b = r & 1
        row = {'a': a, 'b': b}
        if rng.randrange(3) == 0:
            m = {}
            if rng.randrange(2):
                m['a'] = rng.getrandbits(1)
            if rng.randrange(2):
                m['b'] = rng.getrandbits(1)
            if m:
                row['mid'] = m
        rows.append(row)
    return rows[:cycles]
