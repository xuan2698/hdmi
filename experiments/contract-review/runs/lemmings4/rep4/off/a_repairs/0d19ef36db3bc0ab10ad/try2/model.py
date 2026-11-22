def reference(vectors):
    # Moore FSM for Lemmings.
    # States: WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT
    # Outputs are combinational from state.
    # areset is async, active high, positive-edge triggered: when areset rises, state -> WALK_LEFT immediately.
    # We model per-row: each row has inputs driven before the sampled edge.
    # "sample after the posedge edge has settled" -> outputs reflect state after that posedge.
    # Mid changes occur AFTER sampling, before the other edge, carried to start of next row.
    # So: for each row, first apply mid changes from previous row (already applied at end of prev row),
    # then if areset rising edge -> reset state, then compute outputs from state, then apply clock edge transition.

    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)

    state = WALK_LEFT
    fall_count = 0
    prev_areset = 0

    results = []

    def outputs(st):
        # R2_walk_outputs, R3_fall_outputs, R4_dig_outputs, R5_splat_outputs
        if st == WALK_LEFT:
            return {"walk_left": 1, "walk_right": 0, "aaah": 0, "digging": 0}
        elif st == WALK_RIGHT:
            return {"walk_left": 0, "walk_right": 1, "aaah": 0, "digging": 0}
        elif st == FALL_LEFT or st == FALL_RIGHT:
            return {"walk_left": 0, "walk_right": 0, "aaah": 1, "digging": 0}
        elif st == DIG_LEFT or st == DIG_RIGHT:
            return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 1}
        else:  # SPLAT
            return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 0}

    for row in vectors:
        areset = row["areset"]
        bump_left = row["bump_left"]
        bump_right = row["bump_right"]
        ground = row["ground"]
        dig = row["dig"]

        # R1_reset: asynchronous positive-edge reset -> state becomes WALK_LEFT immediately
        if areset == 1 and prev_areset == 0:
            state = WALK_LEFT
            fall_count = 0
        elif areset == 1:
            # held reset: stay in WALK_LEFT
            state = WALK_LEFT
            fall_count = 0

        # Outputs visible same cycle (combinational from state)
        out = outputs(state)
        results.append(out)

        # Now apply posedge transition (unless held in reset)
        if areset == 1:
            # reset holds state at WALK_LEFT
            state = WALK_LEFT
            fall_count = 0
        else:
            # Compute next state
            if state == SPLAT:
                # R14_splat_hold
                pass
            elif state == WALK_LEFT or state == WALK_RIGHT:
                if ground == 0:
                    # R9_walk_fall: fall precedence over dig and bump
                    state = FALL_LEFT if state == WALK_LEFT else FALL_RIGHT
                    fall_count = 0
                elif dig == 1:
                    # R8_walk_start_dig: dig precedence over bump
                    state = DIG_LEFT if state == WALK_LEFT else DIG_RIGHT
                else:
                    # R6_walk_bump_switch, R7_walk_bump_both_switch
                    if bump_left == 1 or bump_right == 1:
                        state = WALK_RIGHT if state == WALK_LEFT else WALK_LEFT
                    # else stay
            elif state == FALL_LEFT or state == FALL_RIGHT:
                if ground == 1:
                    # landing
                    if fall_count > 20:
                        # R11_fall_splat
                        state = SPLAT
                    else:
                        # R10_fall_land
                        state = WALK_LEFT if state == FALL_LEFT else WALK_RIGHT
                    fall_count = 0
                else:
                    # still falling, increment counter
                    fall_count += 1
            elif state == DIG_LEFT or state == DIG_RIGHT:
                if ground == 0:
                    # R13_dig_to_fall
                    state = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
                    fall_count = 0
                # else R12_dig_continue: stay

        prev_areset = areset

    return results
