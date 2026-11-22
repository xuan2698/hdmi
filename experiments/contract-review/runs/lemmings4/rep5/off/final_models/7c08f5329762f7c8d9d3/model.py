def reference(vectors):
    # Moore FSM for Lemmings.
    # States: WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT
    WL, WR, FL, FR, DL, DR, SP = range(7)

    # R1_reset: async reset to WALK_LEFT
    state = WL
    fall_count = 0

    out = []
    for v in vectors:
        areset = v.get('areset', 0)
        bump_left = v.get('bump_left', 0)
        bump_right = v.get('bump_right', 0)
        ground = v.get('ground', 1)
        dig = v.get('dig', 0)

        # R1_reset: async reset visible same cycle
        if areset:
            state = WL
            fall_count = 0

        # Combinational outputs based on current state
        # R2_walk_outputs
        if state == WL:
            o = {'walk_left': 1, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        elif state == WR:
            o = {'walk_left': 0, 'walk_right': 1, 'aaah': 0, 'digging': 0}
        # R3_fall_outputs
        elif state == FL or state == FR:
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 1, 'digging': 0}
        # R4_dig_outputs
        elif state == DL or state == DR:
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 1}
        # R5_splat_outputs
        else:  # SP
            o = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        out.append(o)

        # Posedge transition (skip if reset active this cycle)
        if areset:
            continue

        # R6_walk_transitions
        if state == WL:
            if ground == 0:
                state = FL
                fall_count = 1
            elif dig == 1:
                state = DL
            elif bump_left == 1 or bump_right == 1:
                state = WR
        elif state == WR:
            if ground == 0:
                state = FR
                fall_count = 1
            elif dig == 1:
                state = DR
            elif bump_left == 1 or bump_right == 1:
                state = WL
        # R7_fall_transitions / R9_splat_transition
        elif state == FL:
            if ground == 1:
                if fall_count > 20:
                    state = SP
                else:
                    state = WL
                fall_count = 0
            else:
                fall_count += 1
        elif state == FR:
            if ground == 1:
                if fall_count > 20:
                    state = SP
                else:
                    state = WR
                fall_count = 0
            else:
                fall_count += 1
        # R8_dig_transitions
        elif state == DL:
            if ground == 0:
                state = FL
                fall_count = 1
        elif state == DR:
            if ground == 0:
                state = FR
                fall_count = 1
        # R9_splat_transition: SPLAT stays forever
        elif state == SP:
            pass

    return out
