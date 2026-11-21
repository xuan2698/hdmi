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
    rows.append({'areset':0,'bump_left':1,'bump_right':0,'ground':1,'dig':1})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':1})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0})
    rows.append({'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0})
    while len(rows) < cycles:
        r = {'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0}
        if rng.random() < 0.05:
            r['areset'] = 1
        r['bump_left'] = rng.getrandbits(1)
        r['bump_right'] = rng.getrandbits(1)
        r['ground'] = 1 if rng.random() < 0.7 else 0
        r['dig'] = 1 if rng.random() < 0.2 else 0
        if rng.random() < 0.3:
            m = {}
            if rng.random() < 0.5:
                m['ground'] = rng.getrandbits(1)
            if rng.random() < 0.5:
                m['bump_left'] = rng.getrandbits(1)
            if rng.random() < 0.5:
                m['bump_right'] = rng.getrandbits(1)
            if rng.random() < 0.3:
                m['dig'] = rng.getrandbits(1)
            if m:
                r['mid'] = m
        rows.append(r)
    return rows[:cycles]
