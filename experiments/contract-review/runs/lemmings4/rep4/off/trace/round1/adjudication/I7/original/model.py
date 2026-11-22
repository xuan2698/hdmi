def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)
    state = WALK_LEFT
    fall_count = 0
    outputs = []

    def out_for(st):
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
        # R1_reset: asynchronous reset -> WALK_LEFT, outputs walk_left=1
        if areset:
            state = WALK_LEFT
            fall_count = 0
            outputs.append(out_for(state))
            continue

        # Sample current state outputs (Moore: outputs depend on state)
        outputs.append(out_for(state))

        # Compute next state at posedge
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 0)
        dig = row.get("dig", 0)

        if state == SPLAT:
            # R14_splat_hold
            state = SPLAT
        elif state == WALK_LEFT:
            if ground == 0:
                # R9_walk_fall (fall precedence)
                state = FALL_LEFT
                fall_count = 0
            elif dig == 1:
                # R8_walk_start_dig (dig precedence over bump)
                state = DIG_LEFT
            elif bump_left or bump_right:
                # R6_walk_bump_switch, R7_walk_bump_both_switch
                state = WALK_RIGHT
            else:
                state = WALK_LEFT
        elif state == WALK_RIGHT:
            if ground == 0:
                # R9_walk_fall
                state = FALL_RIGHT
                fall_count = 0
            elif dig == 1:
                # R8_walk_start_dig
                state = DIG_RIGHT
            elif bump_left or bump_right:
                # R6_walk_bump_switch, R7_walk_bump_both_switch
                state = WALK_LEFT
            else:
                state = WALK_RIGHT
        elif state == FALL_LEFT:
            if ground == 1:
                if fall_count > 20:
                    # R11_fall_splat
                    state = SPLAT
                else:
                    # R10_fall_land
                    state = WALK_LEFT
                fall_count = 0
            else:
                fall_count += 1
                state = FALL_LEFT
        elif state == FALL_RIGHT:
            if ground == 1:
                if fall_count > 20:
                    # R11_fall_splat
                    state = SPLAT
                else:
                    # R10_fall_land
                    state = WALK_RIGHT
                fall_count = 0
            else:
                fall_count += 1
                state = FALL_RIGHT
        elif state == DIG_LEFT:
            if ground == 0:
                # R13_dig_to_fall
                state = FALL_LEFT
                fall_count = 0
            else:
                # R12_dig_continue
                state = DIG_LEFT
        elif state == DIG_RIGHT:
            if ground == 0:
                # R13_dig_to_fall
                state = FALL_RIGHT
                fall_count = 0
            else:
                # R12_dig_continue
                state = DIG_RIGHT

    return outputs
