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

    state = WALK_LEFT
    fall_count = 0
    result = []

    for row in vectors:
        areset = row.get("areset", 0)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 1)
        dig = row.get("dig", 0)

        # R1_reset: async reset visible same cycle
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0
            result.append(outputs(state))
            continue

        # Compute next state based on current state and inputs
        if state == SPLAT:
            # R9_splat_transition: stay splatted forever
            next_state = SPLAT
            next_fall = 0
        elif state == WALK_LEFT:
            # R6_walk_transitions: fall > dig > bump
            if ground == 0:
                next_state = FALL_LEFT
                next_fall = 0
            elif dig == 1:
                next_state = DIG_LEFT
                next_fall = 0
            elif bump_left == 1 or bump_right == 1:
                # R6 interpretation: both bumps -> toggle
                next_state = WALK_RIGHT
                next_fall = 0
            else:
                next_state = WALK_LEFT
                next_fall = 0
        elif state == WALK_RIGHT:
            if ground == 0:
                next_state = FALL_RIGHT
                next_fall = 0
            elif dig == 1:
                next_state = DIG_RIGHT
                next_fall = 0
            elif bump_left == 1 or bump_right == 1:
                next_state = WALK_LEFT
                next_fall = 0
            else:
                next_state = WALK_RIGHT
                next_fall = 0
        elif state == FALL_LEFT:
            # R7_fall_transitions, R9_splat_transition
            if ground == 1:
                if fall_count > 20:
                    next_state = SPLAT
                    next_fall = 0
                else:
                    next_state = WALK_LEFT
                    next_fall = 0
            else:
                next_state = FALL_LEFT
                next_fall = fall_count + 1
        elif state == FALL_RIGHT:
            if ground == 1:
                if fall_count > 20:
                    next_state = SPLAT
                    next_fall = 0
                else:
                    next_state = WALK_RIGHT
                    next_fall = 0
            else:
                next_state = FALL_RIGHT
                next_fall = fall_count + 1
        elif state == DIG_LEFT:
            # R8_dig_transitions
            if ground == 0:
                next_state = FALL_LEFT
                next_fall = 0
            else:
                next_state = DIG_LEFT
                next_fall = 0
        elif state == DIG_RIGHT:
            if ground == 0:
                next_state = FALL_RIGHT
                next_fall = 0
            else:
                next_state = DIG_RIGHT
                next_fall = 0
        else:
            next_state = SPLAT
            next_fall = 0

        # Output is based on current state (Moore), visible same cycle
        result.append(outputs(state))

        # Advance state at posedge
        state = next_state
        fall_count = next_fall

    return result
