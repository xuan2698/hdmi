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
        # R1: asynchronous reset (active high) forces WALK_LEFT
        if row.get("areset", 0) == 1:
            state = WALK_LEFT
            fall_count = 0
            results.append(outputs(state))
            continue

        # Sample current outputs (Moore: based on current state)
        results.append(outputs(state))

        # Compute next state on posedge
        bl = row.get("bump_left", 0)
        br = row.get("bump_right", 0)
        g = row.get("ground", 0)
        d = row.get("dig", 0)

        if state == SPLAT:
            # R20: SPLAT stays SPLAT
            next_state = SPLAT
            next_fall = fall_count
        elif state == WALK_LEFT:
            if g == 0:
                # R7: fall precedence
                next_state = FALL_LEFT
                next_fall = 1
            elif d == 1:
                # R9: start digging
                next_state = DIG_LEFT
                next_fall = 0
            elif bl == 1 or br == 1:
                # R11, R13: bump switches direction
                next_state = WALK_RIGHT
                next_fall = 0
            else:
                next_state = WALK_LEFT
                next_fall = 0
        elif state == WALK_RIGHT:
            if g == 0:
                # R8
                next_state = FALL_RIGHT
                next_fall = 1
            elif d == 1:
                # R10
                next_state = DIG_RIGHT
                next_fall = 0
            elif bl == 1 or br == 1:
                # R12, R14
                next_state = WALK_LEFT
                next_fall = 0
            else:
                next_state = WALK_RIGHT
                next_fall = 0
        elif state in (FALL_LEFT, FALL_RIGHT):
            if g == 1:
                # R17: splat if fall_count > 20
                if fall_count > 20:
                    next_state = SPLAT
                    next_fall = 0
                else:
                    # R15, R16: resume walking same direction
                    next_state = WALK_LEFT if state == FALL_LEFT else WALK_RIGHT
                    next_fall = 0
            else:
                next_state = state
                next_fall = fall_count + 1
        elif state in (DIG_LEFT, DIG_RIGHT):
            if g == 0:
                # R18: fall
                next_state = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
                next_fall = 1
            else:
                # R19: stay digging
                next_state = state
                next_fall = 0
        else:
            next_state = state
            next_fall = fall_count

        state = next_state
        fall_count = next_fall

    return results
