def stimulus(rng, cycles):
    rows = []
    def r(**kw):
        d = {'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0}
        d.update(kw)
        return d
    rows.append(r(areset=1))
    rows.append(r())
    rows.append(r(bump_left=1))
    rows.append(r(bump_right=1))
    rows.append(r(bump_left=1,bump_right=1))
    rows.append(r(ground=0))
    rows.append(r(ground=0,bump_left=1))
    rows.append(r(ground=1))
    rows.append(r(dig=1))
    rows.append(r(dig=1,ground=0))
    rows.append(r(ground=0))
    rows.append(r(ground=1))
    rows.append(r(ground=0))
    rows.append(r(ground=0))
    rows.append(r(ground=1))
    rows.append(r(areset=1))
    while len(rows) < cycles:
        d = {'areset':0,'bump_left':0,'bump_right':0,'ground':1,'dig':0}
        if rng.random() < 0.05:
            d['areset'] = 1
        else:
            d['bump_left'] = 1 if rng.random() < 0.2 else 0
            d['bump_right'] = 1 if rng.random() < 0.2 else 0
            d['ground'] = 1 if rng.random() < 0.7 else 0
            d['dig'] = 1 if rng.random() < 0.2 else 0
        if rng.random() < 0.3:
            m = {}
            if rng.random() < 0.5:
                m['ground'] = 1 - d['ground']
            if rng.random() < 0.3:
                m['bump_left'] = 1 - d['bump_left']
            if rng.random() < 0.3:
                m['bump_right'] = 1 - d['bump_right']
            if m:
                d['mid'] = m
        rows.append(d)
    return rows[:cycles]
