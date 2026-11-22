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
    results = []

    for row in vectors:
        areset = row.get("areset", 0)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 1)
        dig = row.get("dig", 0)

        # R1: asynchronous reset forces WALK_LEFT (visible same cycle)
        if areset:
            state = WALK_LEFT
            fall_count = 0

        # Emit outputs for current state (combinational)
        results.append(outputs(state))

        # Compute next state on posedge (visible next cycle)
        if areset:
            # reset already applied; next state stays WALK_LEFT
            state = WALK_LEFT
            fall_count = 0
            continue

        if state == SPLAT:
            # R20: SPLAT stays SPLAT
            state = SPLAT
        elif state == WALK_LEFT:
            if ground == 0:
                # R7: fall precedence
                state = FALL_LEFT
                fall_count = 0
            elif dig == 1:
                # R9
                state = DIG_LEFT
            elif bump_left == 1:
                # R11, R13 (both bumps -> switch)
                state = WALK_RIGHT
            else:
                state = WALK_LEFT
        elif state == WALK_RIGHT:
            if ground == 0:
                # R8
                state = FALL_RIGHT
                fall_count = 0
            elif dig == 1:
                # R10
                state = DIG_RIGHT
            elif bump_right == 1:
                # R12, R14
                state = WALK_LEFT
            else:
                state = WALK_RIGHT
        elif state == FALL_LEFT:
            if ground == 1:
                # R17 splat if fall_count > 20, else R15
                if fall_count > 20:
                    state = SPLAT
                else:
                    state = WALK_LEFT
                fall_count = 0
            else:
                fall_count += 1
                state = FALL_LEFT
        elif state == FALL_RIGHT:
            if ground == 1:
                # R17 / R16
                if fall_count > 20:
                    state = SPLAT
                else:
                    state = WALK_RIGHT
                fall_count = 0
            else:
                fall_count += 1
                state = FALL_RIGHT
        elif state == DIG_LEFT:
            if ground == 0:
                # R18
                state = FALL_LEFT
                fall_count = 0
            else:
                # R19
                state = DIG_LEFT
        elif state == DIG_RIGHT:
            if ground == 0:
                # R18
                state = FALL_RIGHT
                fall_count = 0
            else:
                # R19
                state = DIG_RIGHT

    return results
