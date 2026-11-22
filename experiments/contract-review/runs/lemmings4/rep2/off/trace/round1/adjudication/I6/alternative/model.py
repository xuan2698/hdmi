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
        areset = row["areset"]
        bump_left = row["bump_left"]
        bump_right = row["bump_right"]
        ground = row["ground"]
        dig = row["dig"]

        # R1: asynchronous reset forces WALK_LEFT (visible same cycle)
        if areset:
            state = WALK_LEFT
            fall_count = 0

        # Outputs are combinational from current state (R2-R6)
        result.append(outputs(state))

        # Compute next state on posedge (visible next cycle)
        if areset:
            # Reset already applied; next state stays WALK_LEFT
            state = WALK_LEFT
            fall_count = 0
            continue

        if state == SPLAT:
            # R20: SPLAT stays SPLAT
            state = SPLAT
            continue

        if state == WALK_LEFT:
            if ground == 0:
                # R7: fall precedence over dig
                state = FALL_LEFT
                fall_count = 1
            elif dig == 1:
                # R9: start digging
                state = DIG_LEFT
            elif bump_left == 1:
                # R11, R13: bump left (or both) -> walk right
                state = WALK_RIGHT
            else:
                state = WALK_LEFT
        elif state == WALK_RIGHT:
            if ground == 0:
                # R8: fall
                state = FALL_RIGHT
                fall_count = 1
            elif dig == 1:
                # R10: start digging
                state = DIG_RIGHT
            elif bump_right == 1:
                # R12, R14: bump right (or both) -> walk left
                state = WALK_LEFT
            else:
                state = WALK_RIGHT
        elif state == FALL_LEFT:
            if ground == 1:
                if fall_count > 20:
                    # R17: splat
                    state = SPLAT
                else:
                    # R15: resume walking left
                    state = WALK_LEFT
                fall_count = 0
            else:
                fall_count += 1
                state = FALL_LEFT
        elif state == FALL_RIGHT:
            if ground == 1:
                if fall_count > 20:
                    # R17: splat
                    state = SPLAT
                else:
                    # R16: resume walking right
                    state = WALK_RIGHT
                fall_count = 0
            else:
                fall_count += 1
                state = FALL_RIGHT
        elif state == DIG_LEFT:
            if ground == 0:
                # R18: fall
                state = FALL_LEFT
                fall_count = 1
            else:
                # R19: stay digging
                state = DIG_LEFT
        elif state == DIG_RIGHT:
            if ground == 0:
                # R18: fall
                state = FALL_RIGHT
                fall_count = 1
            else:
                # R19: stay digging
                state = DIG_RIGHT

    return result
