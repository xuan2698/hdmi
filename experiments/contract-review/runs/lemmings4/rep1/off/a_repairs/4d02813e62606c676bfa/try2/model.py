def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)
    
    # Outputs per state: (walk_left, walk_right, aaah, digging)
    outputs = {
        WALK_LEFT:  (1, 0, 0, 0),
        WALK_RIGHT: (0, 1, 0, 0),
        FALL_LEFT:  (0, 0, 1, 0),
        FALL_RIGHT: (0, 0, 1, 0),
        DIG_LEFT:   (0, 0, 0, 1),
        DIG_RIGHT:  (0, 0, 0, 1),
        SPLAT:      (0, 0, 0, 0),
    }
    
    state = WALK_LEFT
    fall_count = 0
    result = []
    
    for row in vectors:
        areset = row.get('areset', 0)
        bump_left = row.get('bump_left', 0)
        bump_right = row.get('bump_right', 0)
        ground = row.get('ground', 1)
        dig = row.get('dig', 0)
        
        # R_RESET: async reset to WALK_LEFT, visible same cycle
        if areset:
            state = WALK_LEFT
            fall_count = 0
        
        # Compute outputs for current state (Moore)
        wl, wr, aa, dg = outputs[state]
        result.append({
            'walk_left': wl,
            'walk_right': wr,
            'aaah': aa,
            'digging': dg,
        })
        
        # Compute next state on posedge
        if areset:
            # reset already applied; next state stays WALK_LEFT
            state = WALK_LEFT
            fall_count = 0
            continue
        
        if state == SPLAT:
            # R_SPLAT_HOLD
            state = SPLAT
            fall_count = 0
            continue
        
        if state in (WALK_LEFT, WALK_RIGHT):
            if ground == 0:
                # R_FALL_START: fall has highest precedence
                fall_count = 1
                state = FALL_LEFT if state == WALK_LEFT else FALL_RIGHT
            elif dig == 1:
                # R_DIG_START: dig next (higher than bump)
                state = DIG_LEFT if state == WALK_LEFT else DIG_RIGHT
                fall_count = 0
            elif bump_left or bump_right:
                # R_BUMP_SWITCH
                state = WALK_RIGHT if state == WALK_LEFT else WALK_LEFT
                fall_count = 0
            else:
                # R_WALK_LEFT / R_WALK_RIGHT: stay
                fall_count = 0
        elif state in (FALL_LEFT, FALL_RIGHT):
            if ground == 0:
                # R_FALL_CONTINUE
                fall_count += 1
                state = FALL_LEFT if state == FALL_LEFT else FALL_RIGHT
            else:
                # ground == 1
                if fall_count > 20:
                    # R_SPLAT
                    state = SPLAT
                    fall_count = 0
                else:
                    # R_FALL_LAND
                    state = WALK_LEFT if state == FALL_LEFT else WALK_RIGHT
                    fall_count = 0
        elif state in (DIG_LEFT, DIG_RIGHT):
            if ground == 0:
                # R_DIG_TO_FALL
                fall_count = 1
                state = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
            else:
                # R_DIG_CONTINUE
                state = DIG_LEFT if state == DIG_LEFT else DIG_RIGHT
                fall_count = 0
    
    return result
