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
    rows.append({'a': 1, 'b': 0, 'mid': {'a': 1, 'b': 1}})
    rows.append({'a': 0, 'b': 1, 'mid': {'a': 0, 'b': 0}})
    rows.append({'a': 1, 'b': 1, 'mid': {'a': 1, 'b': 0}})
    rows.append({'a': 0, 'b': 0, 'mid': {'a': 0, 'b': 1}})
    while len(rows) < cycles:
        r = {'a': rng.getrandbits(1), 'b': rng.getrandbits(1)}
        if rng.random() < 0.5:
            r['mid'] = {'a': rng.getrandbits(1), 'b': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
