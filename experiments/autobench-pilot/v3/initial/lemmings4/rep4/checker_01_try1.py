def reference(vectors):
    state = 'walk_left'
    fall_count = 0
    out = []
    for row in vectors:
        def step(inp):
            nonlocal state, fall_count
            if inp.get('areset'):
                state = 'walk_left'
                fall_count = 0
                return
            if state == 'splatter':
                return
            g = inp.get('ground', 1)
            bl = inp.get('bump_left', 0)
            br = inp.get('bump_right', 0)
            dg = inp.get('dig', 0)
            if state in ('walk_left', 'walk_right'):
                if g == 0:
                    state = 'fall'
                    fall_count = 0
                elif dg:
                    state = 'dig'
                elif bl or br:
                    state = 'walk_right' if state == 'walk_left' else 'walk_left'
            elif state == 'fall':
                if g == 1:
                    if fall_count > 20:
                        state = 'splatter'
                    else:
                        state = 'walk_left' if state == 'fall' else state
                        state = 'walk_left' if getattr(reference, '_dir', 'L') == 'L' else 'walk_right'
                else:
                    fall_count += 1
            elif state == 'dig':
                if g == 0:
                    state = 'fall'
                    fall_count = 0
        step(row)
        if 'mid' in row:
            step(row['mid'])
        if state == 'walk_left':
            o = {'walk_left': 1, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        elif state == 'walk_right':
            o = {'walk_left': 0, 'walk_right': 1, 'aaah': 0, 'digging': 0}
        elif state == 'fall':
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 1, 'digging': 0}
        elif state == 'dig':
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 1}
        else:
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        out.append(o)
    return out
