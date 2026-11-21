def stimulus(rng, cycles):
    rows = []
    rows.append({'areset':1,'bump_left':0,'bump_right':0,'ground':1,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0})
    rows.append({'areset':0,'bump_left':1,'bump_right':0,'ground':1,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':1,'ground':1,'dig':0})
    rows.append({'areset':0,'bump_left':1,'bump_right':1,'ground':1,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0})
    rows.append({'areset':0,'bump_left':1,'bump_right':1,'ground':0,'dig':1})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':1})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0})
    while len(rows) < cycles:
        r = {}
        r['areset'] = 1 if rng.randrange(100) < 2 else 0
        r['bump_left'] = rng.getrandbits(1)
        r['bump_right'] = rng.getrandbits(1)
        r['ground'] = 1 if rng.randrange(100) < 70 else 0
        r['dig'] = 1 if rng.randrange(100) < 20 else 0
        if rng.randrange(100) < 15:
            r['mid'] = {'ground': rng.getrandbits(1)}
        rows.append(r)
    return rows[:cycles]
