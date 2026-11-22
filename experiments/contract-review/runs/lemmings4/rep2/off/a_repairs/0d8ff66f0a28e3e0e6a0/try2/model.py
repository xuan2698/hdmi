def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)

    def outputs(state):
        # R2, R3, R4, R5, R6: combinational outputs per state
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
        areset = row["areset"]
        bump_left = row["bump_left"]
        bump_right = row["bump_right"]
        ground = row["ground"]
        dig = row["dig"]

        # R1: asynchronous reset forces WALK_LEFT, visible same cycle
        if areset:
            state = WALK_LEFT
            fall_count = 0
            result.append(outputs(state))
            continue

        # Outputs are combinational from current state (sampled before edge)
        result.append(outputs(state))

        # Compute next state on posedge
        if state == SPLAT:
            # R20: SPLAT stays SPLAT
            next_state = SPLAT
            next_fall = fall_count
        elif state == WALK_LEFT:
            if ground == 0:
                # R7: fall precedence; R22: bump ignored on ground-disappear cycle
                next_state = FALL_LEFT
                next_fall = 1
            elif dig == 1:
                # R9: start digging
                next_state = DIG_LEFT
                next_fall = 0
            elif bump_left == 1 or bump_right == 1:
                # R11, R13: switch direction (both bumps still switch)
                next_state = WALK_RIGHT
                next_fall = 0
            else:
                next_state = WALK_LEFT
                next_fall = 0
        elif state == WALK_RIGHT:
            if ground == 0:
                # R8: fall; R22: bump ignored
                next_state = FALL_RIGHT
                next_fall = 1
            elif dig == 1:
                # R10: start digging
                next_state = DIG_RIGHT
                next_fall = 0
            elif bump_left == 1 or bump_right == 1:
                # R12, R14: switch direction
                next_state = WALK_LEFT
                next_fall = 0
            else:
                next_state = WALK_RIGHT
                next_fall = 0
        elif state == FALL_LEFT:
            if ground == 1:
                # R15, R17, R23: land; bump ignored
                if fall_count > 20:
                    next_state = SPLAT
                    next_fall = 0
                else:
                    next_state = WALK_LEFT
                    next_fall = 0
            else:
                # R21: bump ignored while falling; dig ignored
                next_state = FALL_LEFT
                next_fall = fall_count + 1
        elif state == FALL_RIGHT:
            if ground == 1:
                # R16, R17, R23
                if fall_count > 20:
                    next_state = SPLAT
                    next_fall = 0
                else:
                    next_state = WALK_RIGHT
                    next_fall = 0
            else:
                # R21
                next_state = FALL_RIGHT
                next_fall = fall_count + 1
        elif state == DIG_LEFT:
            if ground == 0:
                # R18: fall
                next_state = FALL_LEFT
                next_fall = 1
            else:
                # R19, R24: keep digging; bump ignored
                next_state = DIG_LEFT
                next_fall = 0
        elif state == DIG_RIGHT:
            if ground == 0:
                # R18
                next_state = FALL_RIGHT
                next_fall = 1
            else:
                # R19, R24
                next_state = DIG_RIGHT
                next_fall = 0
        else:
            next_state = SPLAT
            next_fall = 0

        state = next_state
        fall_count = next_fall

    return result
