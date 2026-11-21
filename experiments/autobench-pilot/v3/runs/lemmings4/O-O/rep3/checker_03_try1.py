def reference(vectors):
    state = {'dir': 0, 'fall': 0, 'dig': 0, 'splat': 0, 'ft': 0}
    out = []
    for row in vectors:
        def step(inp):
            if inp.get('areset'):
                state.update({'dir': 0, 'fall': 0, 'dig': 0, 'splat': 0, 'ft': 0})
                return
            g = inp.get('ground', 1)
            bl = inp.get('bump_left', 0)
            br = inp.get('bump_right', 0)
            dg = inp.get('dig', 0)
            if state['splat']:
                return
            if state['fall']:
                if g:
                    if state['ft'] > 20:
                        state.update({'splat': 1, 'fall': 0, 'dig': 0, 'ft': 0})
                    else:
                        state.update({'fall': 0, 'ft': 0})
                else:
                    state['ft'] += 1
            elif state['dig']:
                if not g:
                    state.update({'dig': 0, 'fall': 1, 'ft': 0})
            else:
                if not g:
                    state.update({'fall': 1, 'ft': 0})
                elif dg:
                    state['dig'] = 1
                elif bl or br:
                    state['dir'] ^= 1
        step(row)
        o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        if not state['splat']:
            if state['fall']:
                o['aaah'] = 1
            elif state['dig']:
                o['digging'] = 1
            elif state['dir'] == 0:
                o['walk_left'] = 1
            else:
                o['walk_right'] = 1
        out.append(o)
        if 'mid' in row:
            m = dict(row)
            m.update(row['mid'])
            step(m)
    return out
