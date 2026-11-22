def reference(vectors):
    # Moore FSM for Lemmings.
    # States: WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT
    # Outputs are combinational from state (R2-R6).
    # areset is async active-high -> WALK_LEFT (R1).
    # Transitions on posedge (R7-R24).

    WL, WR, FL, FR, DL, DR, SP = range(7)

    def outputs(state):
        # R2: WALK_LEFT outputs
        if state == WL:
            return {"walk_left": 1, "walk_right": 0, "aaah": 0, "digging": 0}
        # R3: WALK_RIGHT outputs
        if state == WR:
            return {"walk_left": 0, "walk_right": 1, "aaah": 0, "digging": 0}
        # R4: FALL_* outputs aaah
        if state in (FL, FR):
            return {"walk_left": 0, "walk_right": 0, "aaah": 1, "digging": 0}
        # R5: DIG_* outputs digging
        if state in (DL, DR):
            return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 1}
        # R6: SPLAT outputs all zero
        return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 0}

    state = WL
    fall_count = 0
    result = []

    for row in vectors:
        areset = row.get("areset", 0)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 0)
        dig = row.get("dig", 0)

        # R1: async reset forces WALK_LEFT (visible same cycle)
        if areset:
            state = WL
            fall_count = 0

        # Combinational outputs for current state
        result.append(outputs(state))

        # Compute next state (posedge transitions)
        if areset:
            # Reset dominates; stay in WL
            state = WL
            fall_count = 0
            continue

        if state == SP:
            # R20: SPLAT stays SPLAT
            state = SP
            continue

        if state == WL:
            if ground == 0:
                # R7: fall precedence; R22: bump ignored on ground-disappear
                state = FL
                fall_count = 1
            elif dig == 1:
                # R9: start digging
                state = DL
                fall_count = 0
            elif bump_left == 1:
                # R11 / R13: bump_left (or both) -> WALK_RIGHT
                state = WR
                fall_count = 0
            else:
                state = WL
                fall_count = 0

        elif state == WR:
            if ground == 0:
                # R8: fall; R22: bump ignored
                state = FR
                fall_count = 1
            elif dig == 1:
                # R10: start digging
                state = DR
                fall_count = 0
            elif bump_right == 1:
                # R12 / R14: bump_right (or both) -> WALK_LEFT
                state = WL
                fall_count = 0
            else:
                state = WR
                fall_count = 0

        elif state == FL:
            if ground == 1:
                # R23: bump ignored on ground-reappear
                if fall_count > 20:
                    # R17: splat
                    state = SP
                    fall_count = 0
                else:
                    # R15: resume walking left
                    state = WL
                    fall_count = 0
            else:
                # R21: bump ignored while falling; dig ignored
                state = FL
                fall_count += 1

        elif state == FR:
            if ground == 1:
                # R23: bump ignored
                if fall_count > 20:
                    # R17: splat
                    state = SP
                    fall_count = 0
                else:
                    # R16: resume walking right
                    state = WR
                    fall_count = 0
            else:
                # R21: bump ignored while falling; dig ignored
                state = FR
                fall_count += 1

        elif state == DL:
            if ground == 0:
                # R18: dig reaches other side -> fall left
                state = FL
                fall_count = 1
            else:
                # R19 / R24: keep digging; bump ignored
                state = DL
                fall_count = 0

        elif state == DR:
            if ground == 0:
                # R18: dig reaches other side -> fall right
                state = FR
                fall_count = 1
            else:
                # R19 / R24: keep digging; bump ignored
                state = DR
                fall_count = 0

    return result
