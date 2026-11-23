def reference(vectors):
    s = 0
    z = 0
    c = {'areset': 0, 'x': 0}
    r = []
    for v in vectors:
        for k in ('areset', 'x'):
            if k in v:
                c[k] = v[k]
        if c['areset']:
            s = 0
            z = 0
        else:
            x = c['x'] & 1
            if s:
                z = 1 - x
            else:
                z = x
                s = x
        r.append({'z': z})
        if 'mid' in v:
            for k in ('areset', 'x'):
                if k in v['mid']:
                    c[k] = v['mid'][k]
            if c['areset']:
                s = 0
                z = 0
    return r
