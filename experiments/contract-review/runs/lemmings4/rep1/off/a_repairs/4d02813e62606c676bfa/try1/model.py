def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)

    def outputs(state):
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
        ground = row.get("ground", 0)
        dig = row.get("dig", 0)

        # R_RESET: async reset visible same cycle
        if areset:
            state = WALK_LEFT
            fall_count = 0
            result.append(outputs(state))
            continue

        # Compute next state based on current state and inputs
        if state == SPLAT:
            # R_SPLAT_HOLD
            next_state = SPLAT
            next_fall = 0
        elif state in (WALK_LEFT, WALK_RIGHT):
            if ground == 0:
                # R_FALL_START (priority over dig and bump)
                next_state = FALL_LEFT if state == WALK_LEFT else FALL_RIGHT
                next_fall = 1
            elif dig == 1:
                # R_DIG_START
                next_state = DIG_LEFT if state == WALK_LEFT else DIG_RIGHT
                next_fall = 0
            elif bump_left or bump_right:
                # R_BUMP_SWITCH
                next_state = WALK_RIGHT if state == WALK_LEFT else WALK_LEFT
                next_fall = 0
            else:
                # R_WALK_LEFT / R_WALK_RIGHT
                next_state = state
                next_fall = 0
        elif state in (FALL_LEFT, FALL_RIGHT):
            if ground == 0:
                # R_FALL_CONTINUE
                next_state = state
                next_fall = fall_count + 1
            else:
                # Landing
                if fall_count > 20:
                    # R_SPLAT
                    next_state = SPLAT
                    next_fall = 0
                else:
                    # R_FALL_LAND
                    next_state = WALK_LEFT if state == FALL_LEFT else WALK_RIGHT
                    next_fall = 0
        elif state in (DIG_LEFT, DIG_RIGHT):
            if ground == 0:
                # R_DIG_TO_FALL
                next_state = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
                next_fall = 1
            else:
                # R_DIG_CONTINUE
                next_state = state
                next_fall = 0
        else:
            next_state = state
            next_fall = 0

        state = next_state
        fall_count = next_fall
        result.append(outputs(state))

    return result
