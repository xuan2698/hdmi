def reference(vectors):
    # Contract rules implemented below:
    # R1_reset: async positive-edge reset -> WALK_LEFT (walk_left=1)
    # R2_walk_outputs: WALK_LEFT/WALK_RIGHT -> walk_left/walk_right
    # R3_fall_outputs: FALL_* -> aaah=1
    # R4_dig_outputs: DIG_* -> digging=1
    # R5_splat_outputs: SPLAT -> all zero
    # R6_walk_bump_switch / R7_walk_bump_both_switch: bump switches direction
    # R8_walk_start_dig: dig has precedence over bump
    # R9_walk_fall: ground=0 -> fall (highest precedence)
    # R10_fall_land: land with counter<=20 -> resume remembered direction
    # R11_fall_splat: land with counter>20 -> SPLAT
    # R12_dig_continue: DIG with ground=1 stays digging
    # R13_dig_to_fall: DIG with ground=0 -> FALL remembered direction
    # R14_splat_hold: SPLAT stays forever

    WALK_LEFT = "WALK_LEFT"
    WALK_RIGHT = "WALK_RIGHT"
    FALL_LEFT = "FALL_LEFT"
    FALL_RIGHT = "FALL_RIGHT"
    DIG_LEFT = "DIG_LEFT"
    DIG_RIGHT = "DIG_RIGHT"
    SPLAT = "SPLAT"

    def outputs(state):
        if state == WALK_LEFT:
            return {"walk_left": 1, "walk_right": 0, "aaah": 0, "digging": 0}
        if state == WALK_RIGHT:
            return {"walk_left": 0, "walk_right": 1, "aaah": 0, "digging": 0}
        if state == FALL_LEFT or state == FALL_RIGHT:
            return {"walk_left": 0, "walk_right": 0, "aaah": 1, "digging": 0}
        if state == DIG_LEFT or state == DIG_RIGHT:
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

        # R1_reset: asynchronous positive-edge reset
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0
            results.append(outputs(state))
            continue

        # Compute next state based on current state and inputs
        if state == SPLAT:
            # R14_splat_hold
            next_state = SPLAT
            next_fall = 0
        elif state == WALK_LEFT or state == WALK_RIGHT:
            if ground == 0:
                # R9_walk_fall (highest precedence)
                next_state = FALL_LEFT if state == WALK_LEFT else FALL_RIGHT
                next_fall = 0
            elif dig == 1:
                # R8_walk_start_dig (precedence over bump)
                next_state = DIG_LEFT if state == WALK_LEFT else DIG_RIGHT
                next_fall = 0
            elif bump_left == 1 or bump_right == 1:
                # R6/R7: switch direction
                next_state = WALK_RIGHT if state == WALK_LEFT else WALK_LEFT
                next_fall = 0
            else:
                next_state = state
                next_fall = 0
        elif state == FALL_LEFT or state == FALL_RIGHT:
            if ground == 1:
                # R10/R11: land
                if fall_count > 20:
                    next_state = SPLAT
                    next_fall = 0
                else:
                    next_state = WALK_LEFT if state == FALL_LEFT else WALK_RIGHT
                    next_fall = 0
            else:
                next_state = state
                next_fall = fall_count + 1
        elif state == DIG_LEFT or state == DIG_RIGHT:
            if ground == 0:
                # R13_dig_to_fall
                next_state = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
                next_fall = 0
            else:
                # R12_dig_continue
                next_state = state
                next_fall = 0
        else:
            next_state = state
            next_fall = 0

        state = next_state
        fall_count = next_fall
        results.append(outputs(state))

    return results
