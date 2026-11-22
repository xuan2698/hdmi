def reference(vectors):
    state = {'dir': 0, 'fall': 0, 'dig': 0, 'dead': 0, 'cnt': 0}
    out = []
    for row in vectors:
        if row.get('areset'):
            state = {'dir': 0, 'fall': 0, 'dig': 0, 'dead': 0, 'cnt': 0}
        else:
            if not state['dead']:
                g = row.get('ground', 1)
                bl = row.get('bump_left', 0)
                br = row.get('bump_right', 0)
                dg = row.get('dig', 0)
                if state['fall']:
                    if g:
                        if state['cnt'] > 20:
                            state['dead'] = 1
                        else:
                            state['fall'] = 0
                            state['cnt'] = 0
                    else:
                        state['cnt'] += 1
                elif state['dig']:
                    if not g:
                        state['dig'] = 0
                        state['fall'] = 1
                        state['cnt'] = 1
                else:
                    if not g:
                        state['fall'] = 1
                        state['cnt'] = 1
                    elif dg:
                        state['dig'] = 1
                    elif bl or br:
                        state['dir'] ^= 1
        o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        if not state['dead']:
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
            m = row['mid']
            if not state['dead']:
                g = m.get('ground', row.get('ground', 1))
                bl = m.get('bump_left', row.get('bump_left', 0))
                br = m.get('bump_right', row.get('bump_right', 0))
                dg = m.get('dig', row.get('dig', 0))
                if state['fall']:
                    if g:
                        if state['cnt'] > 20:
                            state['dead'] = 1
                        else:
                            state['fall'] = 0
                            state['cnt'] = 0
                    else:
                        state['cnt'] += 1
                elif state['dig']:
                    if not g:
                        state['dig'] = 0
                        state['fall'] = 1
                        state['cnt'] = 1
                else:
                    if not g:
                        state['fall'] = 1
                        state['cnt'] = 1
                    elif dg:
                        state['dig'] = 1
                    elif bl or br:
                        state['dir'] ^= 1
    return out
