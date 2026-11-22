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

    state = WALK_LEFT
    fall_count = 0
    result = []

    for row in vectors:
        areset = row.get("areset", 0)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 1)
        dig = row.get("dig", 0)

        # R1_reset: async active-high reset -> WALK_LEFT, visible same cycle
        if areset:
            state = WALK_LEFT
            fall_count = 0
            result.append(outputs(state))
            continue

        # Combinational outputs for current state (sampled before edge)
        result.append(outputs(state))

        # Compute next state on posedge
        ns = state
        nf = fall_count

        if state == WALK_LEFT or state == WALK_RIGHT:
            if ground == 0:
                # R9_walk_fall: fall precedence over dig and bump
                ns = FALL_LEFT if state == WALK_LEFT else FALL_RIGHT
                nf = 0
            elif dig == 1:
                # R8_walk_start_dig: dig precedence over bump
                ns = DIG_LEFT if state == WALK_LEFT else DIG_RIGHT
                nf = 0
            elif bump_left or bump_right:
                # R6_walk_bump_switch, R7_walk_bump_both_switch
                ns = WALK_RIGHT if state == WALK_LEFT else WALK_LEFT
                nf = 0
            else:
                nf = 0
        elif state == FALL_LEFT or state == FALL_RIGHT:
            if ground == 1:
                # R10_fall_land / R11_fall_splat
                if fall_count > 20:
                    ns = SPLAT
                else:
                    ns = WALK_LEFT if state == FALL_LEFT else WALK_RIGHT
                nf = 0
            else:
                # R15_fall_continue
                ns = state
                nf = fall_count + 1
        elif state == DIG_LEFT or state == DIG_RIGHT:
            if ground == 0:
                # R13_dig_to_fall
                ns = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
                nf = 0
            else:
                # R12_dig_continue
                ns = state
                nf = 0
        elif state == SPLAT:
            # R14_splat_hold
            ns = SPLAT
            nf = 0

        state = ns
        fall_count = nf

    return result
