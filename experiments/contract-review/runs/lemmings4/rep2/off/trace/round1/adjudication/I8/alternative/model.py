def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)

    def outputs(state):
        # R2, R3, R4, R5, R6: combinational outputs from state
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
        # R1: asynchronous reset (positive edge triggered, active high)
        if row.get("areset", 0) == 1:
            state = WALK_LEFT
            fall_count = 0
            result.append(outputs(state))
            continue

        # Sample inputs (values driven before this edge)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 0)
        dig = row.get("dig", 0)

        # Compute next state based on current state and inputs
        if state == SPLAT:
            # R20: SPLAT stays SPLAT
            next_state = SPLAT
            next_fall = 0
        elif state == WALK_LEFT:
            if ground == 0:
                # R7: fall precedence
                next_state = FALL_LEFT
                next_fall = 1
            elif dig == 1:
                # R9
                next_state = DIG_LEFT
                next_fall = 0
            elif bump_left == 1:
                # R11, R13 (bump_left covers both-sides case for WALK_LEFT)
                next_state = WALK_RIGHT
                next_fall = 0
            else:
                next_state = WALK_LEFT
                next_fall = 0
        elif state == WALK_RIGHT:
            if ground == 0:
                # R8
                next_state = FALL_RIGHT
                next_fall = 1
            elif dig == 1:
                # R10
                next_state = DIG_RIGHT
                next_fall = 0
            elif bump_right == 1:
                # R12, R14
                next_state = WALK_LEFT
                next_fall = 0
            else:
                next_state = WALK_RIGHT
                next_fall = 0
        elif state == FALL_LEFT:
            if ground == 1:
                if fall_count > 20:
                    # R17
                    next_state = SPLAT
                    next_fall = 0
                else:
                    # R15
                    next_state = WALK_LEFT
                    next_fall = 0
            else:
                next_state = FALL_LEFT
                next_fall = fall_count + 1
        elif state == FALL_RIGHT:
            if ground == 1:
                if fall_count > 20:
                    # R17
                    next_state = SPLAT
                    next_fall = 0
                else:
                    # R16
                    next_state = WALK_RIGHT
                    next_fall = 0
            else:
                next_state = FALL_RIGHT
                next_fall = fall_count + 1
        elif state == DIG_LEFT:
            if ground == 0:
                # R18: transition to FALL on next posedge after ground=0 sampled
                next_state = FALL_LEFT
                next_fall = 1
            else:
                # R19
                next_state = DIG_LEFT
                next_fall = 0
        elif state == DIG_RIGHT:
            if ground == 0:
                # R18
                next_state = FALL_RIGHT
                next_fall = 1
            else:
                # R19
                next_state = DIG_RIGHT
                next_fall = 0
        else:
            next_state = state
            next_fall = fall_count

        # Outputs are combinational from current state (visible same cycle)
        result.append(outputs(state))

        # Advance state at posedge
        state = next_state
        fall_count = next_fall

    return result
