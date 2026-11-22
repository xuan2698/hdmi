def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)

    def outputs(state):
        # R2_walk_outputs, R3_fall_outputs, R4_dig_outputs, R5_splat_outputs
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

    state = WALK_LEFT  # power-up default (walk left)
    fall_count = 0
    results = []

    for row in vectors:
        areset = row["areset"]
        bump_left = row["bump_left"]
        bump_right = row["bump_right"]
        ground = row["ground"]
        dig = row["dig"]

        # R1_reset: asynchronous active-high reset -> WALK_LEFT, visible same cycle
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0
            results.append(outputs(state))
            continue

        # Combinational outputs for current state (sampled before edge)
        results.append(outputs(state))

        # Compute next state (posedge update)
        if state == SPLAT:
            # R14_splat_hold
            next_state = SPLAT
            next_fall = 0
        elif state == WALK_LEFT or state == WALK_RIGHT:
            if ground == 0:
                # R9_walk_fall: fall precedence
                next_state = FALL_LEFT if state == WALK_LEFT else FALL_RIGHT
                next_fall = 1
            elif dig == 1:
                # R8_walk_start_dig: dig precedence over bump
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
                # fall_count counts cycles spent in FALL state (including entry cycle)
                if fall_count > 20:
                    next_state = SPLAT
                else:
                    next_state = WALK_LEFT if state == FALL_LEFT else WALK_RIGHT
                next_fall = 0
            else:
                # R15_fall_continue
                next_state = state
                next_fall = fall_count + 1
        elif state == DIG_LEFT or state == DIG_RIGHT:
            if ground == 0:
                # R13_dig_to_fall
                next_state = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
                next_fall = 1
            else:
                # R12_dig_continue
                next_state = state
                next_fall = 0
        else:
            next_state = state
            next_fall = 0

        state = next_state
        fall_count = next_fall

    return results
