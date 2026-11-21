def reference(vectors):
    st = {'d': 'L', 'm': 'w', 'f': 0, 's': False}
    out = []
    def step(st, ground, bl, br, dig):
        if st['s']:
            return
        if st['m'] == 'w':
            if ground == 0:
                st['m'] = 'f'; st['f'] = 1
            elif dig == 1:
                st['m'] = 'd'
            elif bl == 1 or br == 1:
                st['d'] = 'R' if st['d'] == 'L' else 'L'
        elif st['m'] == 'f':
            if ground == 1:
                if st['f'] > 20:
                    st['s'] = True
                else:
                    st['m'] = 'w'; st['f'] = 0
            else:
                st['f'] += 1
        elif st['m'] == 'd':
            if ground == 0:
                st['m'] = 'f'; st['f'] = 1
    for row in vectors:
        if row.get('areset'):
            st = {'d': 'L', 'm': 'w', 'f': 0, 's': False}
        else:
            step(st, row.get('ground', 1), row.get('bump_left', 0), row.get('bump_right', 0), row.get('dig', 0))
        if st['s']:
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        else:
            o = {
                'walk_left': 1 if st['m'] == 'w' and st['d'] == 'L' else 0,
                'walk_right': 1 if st['m'] == 'w' and st['d'] == 'R' else 0,
                'aaah': 1 if st['m'] == 'f' else 0,
                'digging': 1 if st['m'] == 'd' else 0,
            }
        out.append(o)
        mid = row.get('mid')
        if mid and not st['s']:
            step(st, mid.get('ground', row.get('ground', 1)), mid.get('bump_left', row.get('bump_left', 0)), mid.get('bump_right', row.get('bump_right', 0)), mid.get('dig', row.get('dig', 0)))
    return out
