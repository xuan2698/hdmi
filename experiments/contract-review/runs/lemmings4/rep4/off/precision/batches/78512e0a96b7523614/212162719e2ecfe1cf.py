def reference(vectors):
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)
    state = WALK_LEFT
    fall_count = 0
    out = []
    for v in vectors:
        areset = v.get('areset', 0)
        bump_left = v.get('bump_left', 0)
        bump_right = v.get('bump_right', 0)
        ground = v.get('ground', 1)
        dig = v.get('dig', 0)
        if areset:
            state = WALK_LEFT
            fall_count = 0
        wl = 1 if state == WALK_LEFT else 0
        wr = 1 if state == WALK_RIGHT else 0
        aaah = 1 if state in (FALL_LEFT, FALL_RIGHT) else 0
        digging = 1 if state in (DIG_LEFT, DIG_RIGHT) else 0
        out.append({'walk_left': wl, 'walk_right': wr, 'aaah': aaah, 'digging': digging})
        if areset:
            continue
        if state == WALK_LEFT:
            if ground == 0:
                state = FALL_LEFT
                fall_count = 0
            elif dig == 1:
                state = DIG_LEFT
            elif bump_left or bump_right:
                state = WALK_RIGHT
        elif state == WALK_RIGHT:
            if ground == 0:
                state = FALL_RIGHT
                fall_count = 0
            elif dig == 1:
                state = DIG_RIGHT
            elif bump_left or bump_right:
                state = WALK_LEFT
        elif state == FALL_LEFT:
            if ground == 1:
                if fall_count > 20:
                    state = SPLAT
                else:
                    state = WALK_LEFT
                fall_count = 0
            else:
                fall_count += 1
        elif state == FALL_RIGHT:
            if ground == 1:
                if fall_count > 20:
                    state = SPLAT
                else:
                    state = WALK_RIGHT
                fall_count = 0
            else:
                fall_count += 1
        elif state == DIG_LEFT:
            if ground == 0:
                state = FALL_LEFT
                fall_count = 0
        elif state == DIG_RIGHT:
            if ground == 0:
                state = FALL_RIGHT
                fall_count = 0
        elif state == SPLAT:
            pass
    return out
