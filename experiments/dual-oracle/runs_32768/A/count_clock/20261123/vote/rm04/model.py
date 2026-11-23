def reference(vectors):
    t = 0
    out = []
    for v in vectors:
        if isinstance(v, dict):
            reset = v['reset']
            ena = v['ena']
        else:
            reset, ena = v[0], v[1]

        if reset:
            t = 0
        elif ena:
            t = (t + 1) % 86400

        h = (t // 3600) % 12
        if h == 0:
            h = 12
        m = (t // 60) % 60
        s = t % 60

        def bcd(x):
            return ((x // 10) << 4) | (x % 10)

        out.append({
            'pm': 1 if t >= 43200 else 0,
            'hh': bcd(h),
            'mm': bcd(m),
            'ss': bcd(s)
        })
    return out
