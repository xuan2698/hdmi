def reference(vectors):
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)
    state = WALK_LEFT
    fall_count = 0
    outs = []
    for v in vectors:
        areset = v['areset']
        bl = v['bump_left']
        br = v['bump_right']
        g = v['ground']
        d = v['dig']
        if areset:
            state = WALK_LEFT
            fall_count = 0
        else:
            if state == WALK_LEFT:
                if g == 0:
                    state = FALL_LEFT
                    fall_count = 1
                elif d == 1:
                    state = DIG_LEFT
                elif bl == 1 or br == 1:
                    state = WALK_RIGHT
            elif state == WALK_RIGHT:
                if g == 0:
                    state = FALL_RIGHT
                    fall_count = 1
                elif d == 1:
                    state = DIG_RIGHT
                elif bl == 1 or br == 1:
                    state = WALK_LEFT
            elif state == FALL_LEFT:
                if g == 1:
                    if fall_count > 20:
                        state = SPLAT
                    else:
                        state = WALK_LEFT
                    fall_count = 0
                else:
                    fall_count += 1
            elif state == FALL_RIGHT:
                if g == 1:
                    if fall_count > 20:
                        state = SPLAT
                    else:
                        state = WALK_RIGHT
                    fall_count = 0
                else:
                    fall_count += 1
            elif state == DIG_LEFT:
                if g == 0:
                    state = FALL_LEFT
                    fall_count = 1
            elif state == DIG_RIGHT:
                if g == 0:
                    state = FALL_RIGHT
                    fall_count = 1
            elif state == SPLAT:
                pass
        wl = 1 if state == WALK_LEFT else 0
        wr = 1 if state == WALK_RIGHT else 0
        aa = 1 if state in (FALL_LEFT, FALL_RIGHT) else 0
        dg = 1 if state in (DIG_LEFT, DIG_RIGHT) else 0
        outs.append({'walk_left': wl, 'walk_right': wr, 'aaah': aa, 'digging': dg})
    return outs
