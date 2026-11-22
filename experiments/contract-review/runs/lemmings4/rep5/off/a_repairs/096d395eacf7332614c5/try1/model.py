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

        # R1_reset: async reset to WALK_LEFT
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0
            result.append(outputs(state))
            continue

        # Compute next state based on current state and inputs
        if state == WALK_LEFT:
            # R6_walk_transitions: fall > dig > switch
            if ground == 0:
                state = FALL_LEFT
                fall_count = 0
            elif dig == 1:
                state = DIG_LEFT
            elif bump_left == 1 or bump_right == 1:
                state = WALK_RIGHT
        elif state == WALK_RIGHT:
            if ground == 0:
                state = FALL_RIGHT
                fall_count = 0
            elif dig == 1:
                state = DIG_RIGHT
            elif bump_left == 1 or bump_right == 1:
                state = WALK_LEFT
        elif state == FALL_LEFT:
            # R7_fall_transitions, R9_splat_transition
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
            # R8_dig_transitions
            if ground == 0:
                state = FALL_LEFT
                fall_count = 0
        elif state == DIG_RIGHT:
            if ground == 0:
                state = FALL_RIGHT
                fall_count = 0
        # SPLAT stays SPLAT

        result.append(outputs(state))

    return result
