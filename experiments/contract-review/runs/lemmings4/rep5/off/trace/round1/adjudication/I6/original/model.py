def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)

    # Outputs per state (Moore): walk_left, walk_right, aaah, digging
    OUT = {
        WALK_LEFT:  (1, 0, 0, 0),
        WALK_RIGHT: (0, 1, 0, 0),
        FALL_LEFT:  (0, 0, 1, 0),
        FALL_RIGHT: (0, 0, 1, 0),
        DIG_LEFT:   (0, 0, 0, 1),
        DIG_RIGHT:  (0, 0, 0, 1),
        SPLAT:      (0, 0, 0, 0),
    }

    state = WALK_LEFT   # power-up default (also reset value)
    fall_count = 0
    results = []

    for row in vectors:
        areset    = row.get('areset', 0)
        bump_left = row.get('bump_left', 0)
        bump_right= row.get('bump_right', 0)
        ground    = row.get('ground', 1)
        dig       = row.get('dig', 0)

        # R1_reset: async positive-edge reset -> WALK_LEFT, outputs walk_left=1
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0

        # Combinational outputs for current state (R2/R3/R4/R5)
        wl, wr, aa, dg = OUT[state]
        results.append({
            'walk_left': wl,
            'walk_right': wr,
            'aaah': aa,
            'digging': dg,
        })

        # Compute next state (posedge update)
        if areset == 1:
            # reset already applied; next state stays WALK_LEFT
            next_state = WALK_LEFT
            next_fall = 0
        elif state == SPLAT:
            # R5/R9: stay splatted forever
            next_state = SPLAT
            next_fall = 0
        elif state in (WALK_LEFT, WALK_RIGHT):
            # R6_walk_transitions: fall > dig > bump
            if ground == 0:
                next_state = FALL_LEFT if state == WALK_LEFT else FALL_RIGHT
                next_fall = 1
            elif dig == 1:
                next_state = DIG_LEFT if state == WALK_LEFT else DIG_RIGHT
                next_fall = 0
            elif bump_left == 1 or bump_right == 1:
                # bump on either side (or both) -> switch direction
                next_state = WALK_RIGHT if state == WALK_LEFT else WALK_LEFT
                next_fall = 0
            else:
                next_state = state
                next_fall = 0
        elif state in (FALL_LEFT, FALL_RIGHT):
            # R7_fall_transitions / R9_splat_transition
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
            # R8_dig_transitions
            if ground == 0:
                next_state = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
                next_fall = 1
            else:
                next_state = state
                next_fall = 0
        else:
            next_state = state
            next_fall = 0

        state = next_state
        fall_count = next_fall

    return results
