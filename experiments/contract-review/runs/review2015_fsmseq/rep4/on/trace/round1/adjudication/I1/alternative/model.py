def reference(vectors):
    # State encodings with named FSM states.
    S0 = 0
    S1 = 1
    S11 = 2
    S110 = 3
    FOUND = 4

    state = S0
    start_shifting = 0
    cur_reset = 0
    cur_data = 0
    result = []

    for row in vectors:
        # Drive this row's pre-posedge input values.
        if "reset" in row:
            cur_reset = row["reset"] & 1
        if "data" in row:
            cur_data = row["data"] & 1

        # r_reset_clear: active-high synchronous reset forces S0 and clears output.
        if cur_reset == 1:
            nxt_state = S0
            nxt_start_shifting = 0
        else:
            # r_set_or_hold: next_cycle interpretation. Assert only after a prior
            # completion has moved the FSM into FOUND.
            if state == FOUND:
                nxt_state = FOUND
                nxt_start_shifting = 1
            else:
                # Explicit FSM transitions for 1101 detection.
                if state == S0:
                    nxt_state = S1 if cur_data == 1 else S0
                elif state == S1:
                    nxt_state = S11 if cur_data == 1 else S0
                elif state == S11:
                    nxt_state = S110 if cur_data == 0 else S11
                elif state == S110:
                    nxt_state = FOUND if cur_data == 1 else S0
                else:
                    nxt_state = S0

                # r_default_clear: clear output unless held by FOUND. Under the
                # selected next_cycle interpretation, completion this edge enters
                # FOUND but does not assert start_shifting until the next posedge.
                nxt_start_shifting = 0

        # Register updates after the sampled posedge.
        state = nxt_state
        start_shifting = nxt_start_shifting
        result.append({"start_shifting": start_shifting})

        # Apply optional mid-cycle changes after sampling; they persist to the
        # start of the next row unless overwritten by that row's driven values.
        mid = row.get("mid")
        if mid is not None:
            if "reset" in mid:
                cur_reset = mid["reset"] & 1
            if "data" in mid:
                cur_data = mid["data"] & 1

    return result
