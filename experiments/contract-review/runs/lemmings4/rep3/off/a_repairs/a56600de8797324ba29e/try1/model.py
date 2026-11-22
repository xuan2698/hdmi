def reference(vectors):
    # Contract implementation for Lemmings FSM.
    # States: WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT
    WL, WR, FL, FR, DL, DR, SP = range(7)

    def outputs(state):
        # R2_walk_outputs, R3_fall_outputs, R4_dig_outputs, R5_splat_outputs
        if state == WL:
            return {"walk_left": 1, "walk_right": 0, "aaah": 0, "digging": 0}
        if state == WR:
            return {"walk_left": 0, "walk_right": 1, "aaah": 0, "digging": 0}
        if state in (FL, FR):
            return {"walk_left": 0, "walk_right": 0, "aaah": 1, "digging": 0}
        if state in (DL, DR):
            return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 1}
        # SPLAT
        return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 0}

    state = WL
    fall_count = 0
    result = []

    for row in vectors:
        areset = row.get("areset", 0)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 1)
        dig = row.get("dig", 0)

        # R1_reset: async positive-edge reset -> WALK_LEFT
        if areset == 1:
            state = WL
            fall_count = 0
            result.append(outputs(state))
            continue

        # Compute next state (posedge update)
        if state == WL or state == WR:
            if ground == 0:
                # R7_walk_to_fall: fall has precedence
                state = FL if state == WL else FR
                fall_count = 0
            elif dig == 1:
                # R6_walk_transition: dig precedence over bump
                state = DL if state == WL else DR
            elif bump_left == 1 or bump_right == 1:
                # R6_walk_transition: switch direction
                state = WR if state == WL else WL
            # else keep direction
        elif state == FL or state == FR:
            if ground == 1:
                # R8_fall_transition
                if fall_count > 20:
                    state = SP
                else:
                    state = WL if state == FL else WR
                fall_count = 0
            else:
                fall_count += 1
        elif state == DL or state == DR:
            if ground == 0:
                # R9_dig_transition
                state = FL if state == DL else FR
                fall_count = 0
            # else stay digging
        elif state == SP:
            # R10_splat_stay
            pass

        result.append(outputs(state))

    return result
