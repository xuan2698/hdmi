def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)
    state = WALK_LEFT
    fall_count = 0
    prev_dig = 0
    results = []

    def outputs(st):
        # R2_walk_outputs, R3_fall_outputs, R4_dig_outputs, R5_splat_outputs
        if st == WALK_LEFT:
            return {"walk_left": 1, "walk_right": 0, "aaah": 0, "digging": 0}
        if st == WALK_RIGHT:
            return {"walk_left": 0, "walk_right": 1, "aaah": 0, "digging": 0}
        if st in (FALL_LEFT, FALL_RIGHT):
            return {"walk_left": 0, "walk_right": 0, "aaah": 1, "digging": 0}
        if st in (DIG_LEFT, DIG_RIGHT):
            return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 1}
        # SPLAT
        return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 0}

    for row in vectors:
        areset = row.get("areset", 0)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 0)
        dig = row.get("dig", 0)

        # R1_reset: asynchronous positive-edge reset -> WALK_LEFT
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0
            prev_dig = dig
            results.append(outputs(state))
            continue

        # Compute next state based on current state and inputs
        if state == SPLAT:
            # R14_splat_hold
            next_state = SPLAT
            next_fall = fall_count
        elif state == WALK_LEFT or state == WALK_RIGHT:
            if ground == 0:
                # R9_walk_fall: fall precedence
                next_state = FALL_LEFT if state == WALK_LEFT else FALL_RIGHT
                next_fall = 0
            elif dig == 1 and prev_dig == 0:
                # R8_walk_start_dig: dig starts only on 0->1 transition
                next_state = DIG_LEFT if state == WALK_LEFT else DIG_RIGHT
                next_fall = 0
            elif bump_left == 1 or bump_right == 1:
                # R6_walk_bump_switch, R7_walk_bump_both_switch
                next_state = WALK_RIGHT if state == WALK_LEFT else WALK_LEFT
                next_fall = 0
            else:
                next_state = state
                next_fall = 0
        elif state == FALL_LEFT or state == FALL_RIGHT:
            if ground == 1:
                # R10_fall_land / R11_fall_splat
                if fall_count > 20:
                    next_state = SPLAT
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
            next_fall = fall_count

        state = next_state
        fall_count = next_fall
        prev_dig = dig
        results.append(outputs(state))

    return results
