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
    results = []

    for v in vectors:
        areset = v.get("areset", 0)
        bump_left = v.get("bump_left", 0)
        bump_right = v.get("bump_right", 0)
        ground = v.get("ground", 1)
        dig = v.get("dig", 0)

        # R1_reset: async positive edge triggered reset to WALK_LEFT
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0
            results.append(outputs(state))
            continue

        # Compute next state based on current state and inputs (posedge update)
        if state == SPLAT:
            # R5_splat_outputs: stays splatted forever
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
        elif state in (FALL_LEFT, FALL_RIGHT):
            # R7_fall_transitions: ground=1 -> resume walk same dir (splat if >20)
            # R9_splat_transition: fall duration > 20 cycles -> SPLAT
            if ground == 1:
                if fall_count > 20:
                    next_state = SPLAT
                    next_fall = 0
                else:
                    next_state = WALK_LEFT if state == FALL_LEFT else WALK_RIGHT
                    next_fall = 0
            else:
                next_state = state
                next_fall = fall_count + 1
        elif state in (DIG_LEFT, DIG_RIGHT):
            # R8_dig_transitions: ground=0 -> fall same dir; else stay digging
            if ground == 0:
                next_state = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
                next_fall = 0
            else:
                next_state = state
                next_fall = 0
        else:
            next_state = state
            next_fall = 0

        # Output is based on current state (Moore, combinational visible same cycle)
        results.append(outputs(state))

        # Apply posedge update
        state = next_state
        fall_count = next_fall

    return results
