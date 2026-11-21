def reference(vectors):
    st = {'d': 0, 'f': 0, 'g': 0, 'x': 0, 'c': 0}
    out = []
    for row in vectors:
        if row.get('areset'):
            st = {'d': 0, 'f': 0, 'g': 0, 'x': 0, 'c': 0}
        else:
            if not st['x']:
                g = row.get('ground', 1)
                bl = row.get('bump_left', 0)
                br = row.get('bump_right', 0)
                dg = row.get('dig', 0)
                if st['f']:
                    if g:
                        if st['c'] > 20:
                            st['x'] = 1
                        else:
                            st['f'] = 0
                            st['c'] = 0
                    else:
                        st['c'] += 1
                elif st['g']:
                    if not g:
                        st['g'] = 0
                        st['f'] = 1
                        st['c'] = 1
                else:
                    if not g:
                        st['f'] = 1
                        st['c'] = 1
                    elif dg:
                        st['g'] = 1
                    elif bl or br:
                        st['d'] ^= 1
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
            if not st['x']:
                g = m.get('ground', row.get('ground', 1))
                bl = m.get('bump_left', row.get('bump_left', 0))
                br = m.get('bump_right', row.get('bump_right', 0))
                dg = m.get('dig', row.get('dig', 0))
                if st['f']:
                    if g:
                        if st['c'] > 20:
                            st['x'] = 1
                        else:
                            st['f'] = 0
                            st['c'] = 0
                    else:
                        st['c'] += 1
                elif st['g']:
                    if not g:
                        st['g'] = 0
                        st['f'] = 1
                        st['c'] = 1
                else:
                    if not g:
                        st['f'] = 1
                        st['c'] = 1
                    elif dg:
                        st['g'] = 1
                    elif bl or br:
                        st['d'] ^= 1
    return out
