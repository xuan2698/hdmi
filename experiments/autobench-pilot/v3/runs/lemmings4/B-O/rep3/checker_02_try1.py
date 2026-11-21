def reference(vectors):
    st = {'d': 0, 'f': 0, 'g': 0, 's': 0, 't': 0}
    out = []
    def step(st, g, bl, br, dg):
        if st['s']:
            return
        if st['f']:
            if g:
                if st['t'] > 20:
                    st['s'] = 1; st['f'] = 0; st['g'] = 0; st['t'] = 0
                else:
                    st['f'] = 0; st['t'] = 0
            else:
                st['t'] += 1
        elif st['g']:
            if not g:
                st['g'] = 0; st['f'] = 1; st['t'] = 0
        else:
            if not g:
                st['f'] = 1; st['t'] = 0
            elif dg:
                st['g'] = 1
            elif bl or br:
                st['d'] ^= 1
    for row in vectors:
        if row.get('areset'):
            st = {'d': 0, 'f': 0, 'g': 0, 's': 0, 't': 0}
        else:
            step(st, row.get('ground', 1), row.get('bump_left', 0), row.get('bump_right', 0), row.get('dig', 0))
        o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        if not st['s']:
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
            if m.get('areset'):
                st = {'d': 0, 'f': 0, 'g': 0, 's': 0, 't': 0}
            else:
                step(st, m.get('ground', row.get('ground', 1)), m.get('bump_left', row.get('bump_left', 0)), m.get('bump_right', row.get('bump_right', 0)), m.get('dig', row.get('dig', 0)))
    return out
