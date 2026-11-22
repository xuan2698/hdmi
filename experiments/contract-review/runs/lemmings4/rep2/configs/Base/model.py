def reference(vectors):
    state = {'dir': 'L', 'mode': 'walk', 'fall': 0, 'splat': False}
    out = []
    for row in vectors:
        def step(inp):
            if inp.get('areset'):
                state.update(dir='L', mode='walk', fall=0, splat=False)
                return
            if state['splat']:
                return
            g = inp.get('ground', 1)
            bl = inp.get('bump_left', 0)
            br = inp.get('bump_right', 0)
            dg = inp.get('dig', 0)
            if state['mode'] == 'fall':
                if g:
                    if state['fall'] > 20:
                        state['splat'] = True
                        state['mode'] = 'splat'
                    else:
                        state['mode'] = 'walk'
                        state['fall'] = 0
                else:
                    state['fall'] += 1
            elif state['mode'] == 'dig':
                if not g:
                    state['mode'] = 'fall'
                    state['fall'] = 1
            else:
                if not g:
                    state['mode'] = 'fall'
                    state['fall'] = 1
                elif dg:
                    state['mode'] = 'dig'
                elif bl or br:
                    state['dir'] = 'R' if state['dir'] == 'L' else 'L'
        step(row)
        if 'mid' in row:
            step(row['mid'])
        o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        if not state['splat']:
            if state['mode'] == 'walk':
                o['walk_left'] = 1 if state['dir'] == 'L' else 0
                o['walk_right'] = 1 if state['dir'] == 'R' else 0
            elif state['mode'] == 'fall':
                o['aaah'] = 1
            elif state['mode'] == 'dig':
                o['digging'] = 1
        out.append(o)
    return out
