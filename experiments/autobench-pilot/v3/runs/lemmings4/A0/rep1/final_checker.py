def reference(vectors):
    state = {'dir': 0, 'fall': 0, 'dig': 0, 'splat': 0, 'cnt': 0}
    out = []
    def step(inp, mid=None):
        if inp.get('areset'):
            state.update({'dir': 0, 'fall': 0, 'dig': 0, 'splat': 0, 'cnt': 0})
            return
        if state['splat']:
            return
        g = inp.get('ground', 1)
        bl = inp.get('bump_left', 0)
        br = inp.get('bump_right', 0)
        dg = inp.get('dig', 0)
        if state['fall']:
            if g:
                if state['cnt'] > 20:
                    state['splat'] = 1
                else:
                    state['fall'] = 0
                    state['cnt'] = 0
            else:
                state['cnt'] += 1
        elif state['dig']:
            if not g:
                state['dig'] = 0
                state['fall'] = 1
                state['cnt'] = 0
        else:
            if not g:
                state['fall'] = 1
                state['cnt'] = 0
            elif dg:
                state['dig'] = 1
            elif bl or br:
                state['dir'] ^= 1
    for row in vectors:
        step(row)
        if 'mid' in row:
            step(row['mid'])
        if state['splat']:
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        elif state['fall']:
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 1, 'digging': 0}
        elif state['dig']:
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 1}
        else:
            o = {'walk_left': 1 - state['dir'], 'walk_right': state['dir'], 'aaah': 0, 'digging': 0}
        out.append(o)
    return out
