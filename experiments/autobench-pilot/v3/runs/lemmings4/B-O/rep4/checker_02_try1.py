def reference(vectors):
    state = {'dir': 'L', 'mode': 'walk', 'fall_count': 0, 'splattered': False}
    out = []
    for row in vectors:
        if row.get('areset'):
            state = {'dir': 'L', 'mode': 'walk', 'fall_count': 0, 'splattered': False}
        else:
            if not state['splattered']:
                ground = row.get('ground', 1)
                bl = row.get('bump_left', 0)
                br = row.get('bump_right', 0)
                dig = row.get('dig', 0)
                if state['mode'] == 'walk':
                    if ground == 0:
                        state['mode'] = 'fall'
                        state['fall_count'] = 1
                    elif dig == 1:
                        state['mode'] = 'dig'
                    elif bl == 1 or br == 1:
                        state['dir'] = 'R' if state['dir'] == 'L' else 'L'
                elif state['mode'] == 'fall':
                    if ground == 1:
                        if state['fall_count'] > 20:
                            state['splattered'] = True
                        else:
                            state['mode'] = 'walk'
                            state['fall_count'] = 0
                    else:
                        state['fall_count'] += 1
                elif state['mode'] == 'dig':
                    if ground == 0:
                        state['mode'] = 'fall'
                        state['fall_count'] = 1
        if state['splattered']:
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        else:
            o = {
                'walk_left': 1 if state['mode'] == 'walk' and state['dir'] == 'L' else 0,
                'walk_right': 1 if state['mode'] == 'walk' and state['dir'] == 'R' else 0,
                'aaah': 1 if state['mode'] == 'fall' else 0,
                'digging': 1 if state['mode'] == 'dig' else 0,
            }
        out.append(o)
        mid = row.get('mid')
        if mid and not state['splattered']:
            ground = mid.get('ground', row.get('ground', 1))
            bl = mid.get('bump_left', row.get('bump_left', 0))
            br = mid.get('bump_right', row.get('bump_right', 0))
            dig = mid.get('dig', row.get('dig', 0))
            if state['mode'] == 'walk':
                if ground == 0:
                    state['mode'] = 'fall'
                    state['fall_count'] = 1
                elif dig == 1:
                    state['mode'] = 'dig'
                elif bl == 1 or br == 1:
                    state['dir'] = 'R' if state['dir'] == 'L' else 'L'
            elif state['mode'] == 'fall':
                if ground == 1:
                    if state['fall_count'] > 20:
                        state['splattered'] = True
                    else:
                        state['mode'] = 'walk'
                        state['fall_count'] = 0
                else:
                    state['fall_count'] += 1
            elif state['mode'] == 'dig':
                if ground == 0:
                    state['mode'] = 'fall'
                    state['fall_count'] = 1
    return out
