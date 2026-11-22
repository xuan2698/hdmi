def reference(vectors):
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)
    state = WALK_LEFT
    fall_count = 0
    outs = []
    for v in vectors:
        areset = v['areset']
        bump_left = v['bump_left']
        bump_right = v['bump_right']
        ground = v['ground']
        dig = v['dig']
        if areset:
            state = WALK_LEFT
            fall_count = 0
        if state == WALK_LEFT:
            o = (1,0,0,0)
        elif state == WALK_RIGHT:
            o = (0,1,0,0)
        elif state in (FALL_LEFT, FALL_RIGHT):
            o = (0,0,1,0)
        elif state in (DIG_LEFT, DIG_RIGHT):
            o = (0,0,0,1)
        else:
            o = (0,0,0,0)
        outs.append({'walk_left':o[0],'walk_right':o[1],'aaah':o[2],'digging':o[3]})
        if areset:
            continue
        ns = state
        if state == WALK_LEFT:
            if ground == 0:
                ns = FALL_LEFT
                fall_count = 1
            elif dig == 1:
                ns = DIG_LEFT
            elif bump_left == 1 or bump_right == 1:
                ns = WALK_RIGHT
        elif state == WALK_RIGHT:
            if ground == 0:
                ns = FALL_RIGHT
                fall_count = 1
            elif dig == 1:
                ns = DIG_RIGHT
            elif bump_left == 1 or bump_right == 1:
                ns = WALK_LEFT
        elif state == FALL_LEFT:
            if ground == 1:
                if fall_count > 20:
                    ns = SPLAT
                else:
                    ns = WALK_LEFT
                fall_count = 0
            else:
                fall_count += 1
        elif state == FALL_RIGHT:
            if ground == 1:
                if fall_count > 20:
                    ns = SPLAT
                else:
                    ns = WALK_RIGHT
                fall_count = 0
            else:
                fall_count += 1
        elif state == DIG_LEFT:
            if ground == 0:
                ns = FALL_LEFT
                fall_count = 1
        elif state == DIG_RIGHT:
            if ground == 0:
                ns = FALL_RIGHT
                fall_count = 1
        state = ns
    return outs
