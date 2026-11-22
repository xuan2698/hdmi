def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)
    state = WALK_LEFT
    fall_count = 0

    def outputs(st):
        # R2_walk_outputs, R3_fall_outputs, R4_dig_outputs, R5_splat_outputs
        if st == WALK_LEFT:
            return {"walk_left": 1, "walk_right": 0, "aaah": 0, "digging": 0}
        if st == WALK_RIGHT:
            return {"walk_left": 0, "walk_right": 1, "aaah": 0, "digging": 0}
        if st == FALL_LEFT or st == FALL_RIGHT:
            return {"walk_left": 0, "walk_right": 0, "aaah": 1, "digging": 0}
        if st == DIG_LEFT or st == DIG_RIGHT:
            return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 1}
        # SPLAT
        return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 0}

    result = []
    for row in vectors:
        areset = row.get("areset", 0)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 1)
        dig = row.get("dig", 0)

        # R1_reset: async reset -> WALK_LEFT, visible same cycle
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0
            result.append(outputs(state))
            continue

        # Compute next state based on current state and inputs (posedge update)
        if state == SPLAT:
            # R9_splat_transition: stay splatted forever
            next_state = SPLAT
            next_fall = 0
        elif state == WALK_LEFT or state == WALK_RIGHT:
            # R6_walk_transitions: fall > dig > switch
            if ground == 0:
                next_state = FALL_LEFT if state == WALK_LEFT else FALL_RIGHT
                next_fall = 0
            elif dig == 1:
                next_state = DIG_LEFT if state == WALK_LEFT else DIG_RIGHT
                next_fall = 0
            else:
                if bump_left == 1 and bump_right == 1:
                    # switch direction
                    next_state = WALK_RIGHT if state == WALK_LEFT else WALK_LEFT
                elif bump_left == 1:
                    next_state = WALK_RIGHT
                elif bump_right == 1:
                    next_state = WALK_LEFT
                else:
                    next_state = state
                next_fall = 0
        elif state == FALL_LEFT or state == FALL_RIGHT:
            # R7_fall_transitions, R9_splat_transition
            if ground == 1:
                # fell for fall_count cycles; splat if > 20
                if fall_count > 20:
                    next_state = SPLAT
                else:
                    next_state = WALK_LEFT if state == FALL_LEFT else WALK_RIGHT
                next_fall = 0
            else:
                next_state = state
                next_fall = fall_count + 1
        elif state == DIG_LEFT or state == DIG_RIGHT:
            # R8_dig_transitions
            if ground == 0:
                next_state = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
                next_fall = 0
            else:
                next_state = state
                next_fall = 0
        else:
            next_state = state
            next_fall = 0

        # Outputs are combinational from current state (Moore)
        result.append(outputs(state))

        # Apply posedge update
        state = next_state
        fall_count = next_fall

    return result
