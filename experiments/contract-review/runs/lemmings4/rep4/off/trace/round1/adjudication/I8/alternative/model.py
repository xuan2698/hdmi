def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)
    
    def outputs(state):
        # R2_walk_outputs, R3_fall_outputs, R4_dig_outputs, R5_splat_outputs
        if state == WALK_LEFT:
            return {"walk_left": 1, "walk_right": 0, "aaah": 0, "digging": 0}
        if state == WALK_RIGHT:
            return {"walk_left": 0, "walk_right": 1, "aaah": 0, "digging": 0}
        if state in (FALL_LEFT, FALL_RIGHT):
            return {"walk_left": 0, "walk_right": 0, "aaah": 1, "digging": 0}
        if state in (DIG_LEFT, DIG_RIGHT):
            return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 1}
        # SPLAT
        return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 0}
    
    state = WALK_LEFT  # power-up default (will be reset by areset)
    fall_count = 0
    results = []
    
    for vec in vectors:
        areset = vec["areset"]
        bump_left = vec["bump_left"]
        bump_right = vec["bump_right"]
        ground = vec["ground"]
        dig = vec["dig"]
        
        # R1_reset: asynchronous positive-edge reset -> walk left
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0
            results.append(outputs(state))
            continue
        
        # Compute next state based on current state and inputs
        next_state = state
        next_fall_count = fall_count
        
        if state == WALK_LEFT or state == WALK_RIGHT:
            if ground == 0:
                # R9_walk_fall: fall has highest precedence
                # Candidate interpretation: if bump occurs same cycle, remember switched direction
                if state == WALK_LEFT:
                    if bump_left == 1 or bump_right == 1:
                        next_state = FALL_RIGHT
                    else:
                        next_state = FALL_LEFT
                else:
                    if bump_left == 1 or bump_right == 1:
                        next_state = FALL_LEFT
                    else:
                        next_state = FALL_RIGHT
                next_fall_count = 0
            elif dig == 1:
                # R8_walk_start_dig: dig precedence over bump
                if state == WALK_LEFT:
                    next_state = DIG_LEFT
                else:
                    next_state = DIG_RIGHT
            elif bump_left == 1 or bump_right == 1:
                # R6_walk_bump_switch, R7_walk_bump_both_switch
                if state == WALK_LEFT:
                    next_state = WALK_RIGHT
                else:
                    next_state = WALK_LEFT
            # else stay
        elif state == FALL_LEFT or state == FALL_RIGHT:
            if ground == 1:
                # R10_fall_land / R11_fall_splat
                if fall_count > 20:
                    next_state = SPLAT
                else:
                    if state == FALL_LEFT:
                        next_state = WALK_LEFT
                    else:
                        next_state = WALK_RIGHT
                next_fall_count = 0
            else:
                next_fall_count = fall_count + 1
        elif state == DIG_LEFT or state == DIG_RIGHT:
            if ground == 0:
                # R13_dig_to_fall
                if state == DIG_LEFT:
                    next_state = FALL_LEFT
                else:
                    next_state = FALL_RIGHT
                next_fall_count = 0
            # else R12_dig_continue: stay digging
        elif state == SPLAT:
            # R14_splat_hold
            next_state = SPLAT
        
        state = next_state
        fall_count = next_fall_count
        results.append(outputs(state))
    
    return results
