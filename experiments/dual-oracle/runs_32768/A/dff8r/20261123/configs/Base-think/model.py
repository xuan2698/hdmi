def reference(vectors):
    q = 0
    s = {'d': 0, 'reset': 0}
    out = []
    for r in vectors:
        for k in ('d', 'reset'):
            if k in r:
                s[k] = r[k]
        d = s['d'] & 255
        reset = s['reset'] & 1
        if reset:
            q = 0
        else:
            q = d
        out.append({'q': q & 255})
        if 'mid' in r:
            for k, v in r['mid'].items():
                if k in s:
                    s[k] = v
    return out
