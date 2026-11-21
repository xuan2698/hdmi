def stimulus(rng, cycles):
    rows = []
    rows.append({'areset': 1, 'bump_left': 0, 'bump_right': 0, 'ground': 1, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 1, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 1, 'bump_right': 0, 'ground': 1, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 1, 'ground': 1, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 1, 'bump_right': 1, 'ground': 1, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 0, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 1, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 1, 'dig': 1})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 0, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 1, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 0, 'dig': 0, 'mid': {'ground': 1}})
    rows.append({'areset': 0, 'bump_left': 1, 'bump_right': 0, 'ground': 1, 'dig': 0, 'mid': {'bump_left': 0}})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 0, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 0, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 0, 'dig': 0})
    rows.append({'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 0, 'dig': 0})
    while len(rows) < cycles:
        r = {'areset': 0}
        r['bump_left'] = rng.getrandbits(1)
        r['bump_right'] = rng.getrandbits(1)
        r['ground'] = rng.getrandbits(1)
        r['dig'] = rng.getrandbits(1)
        if rng.random() < 0.3:
            r['mid'] = {'ground': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
