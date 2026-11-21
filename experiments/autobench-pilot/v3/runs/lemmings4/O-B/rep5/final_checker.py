def reference(vectors):
    st = {'d': 0, 'f': 0, 'g': 0, 'x': 0, 'c': 0}
    out = []
    def step(s, g, bl, br, dg):
        if s['x']:
            return
        if s['f']:
            if g:
                if s['c'] > 20:
                    s['x'] = 1
                else:
                    s['f'] = 0
                    s['c'] = 0
            else:
                s['c'] += 1
        elif s['g']:
            if not g:
                s['g'] = 0
                s['f'] = 1
                s['c'] = 1
        else:
            if not g:
                s['f'] = 1
                s['c'] = 1
            elif dg:
                s['g'] = 1
            elif bl or br:
                s['d'] ^= 1
    for row in vectors:
        if row.get('areset'):
            st = {'d': 0, 'f': 0, 'g': 0, 'x': 0, 'c': 0}
        else:
            step(st, row.get('ground', 1), row.get('bump_left', 0), row.get('bump_right', 0), row.get('dig', 0))
        o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        if not st['x']:
            if st['f']:
                o['aaah'] = 1
            elif st['g']:
                o['digging'] = 1
            elif st['d'] == 0:
                o['walk_left'] = 1
            else:
                o['walk_right'] = 1
        out.append(o)
        if 'mid' in row:
            m = row['mid']
            step(st, m.get('ground', row.get('ground', 1)), m.get('bump_left', row.get('bump_left', 0)), m.get('bump_right', row.get('bump_right', 0)), m.get('dig', row.get('dig', 0)))
    return out
