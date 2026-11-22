def reference(vectors):
    # State encoding
    S0 = 0
    S1 = 1
    S11 = 2
    S110 = 3
    FOUND = 4

    state = S0
    cur_reset = 0
    cur_data = 0
    outputs = []

    for row in vectors:
        # Row inputs are driven before the sampled posedge.
        if "reset" in row:
            cur_reset = row["reset"]
        if "data" in row:
            cur_data = row["data"]

        reset = cur_reset
        data = cur_data

        # Compute next state after the sampled posedge.
        if reset == 1:
            # r_reset_clear: synchronous active-high reset has priority 0.
            next_state = S0
        else:
            if state == S0:
                if data == 1:
                    next_state = S1
                else:
                    next_state = S0
            elif state == S1:
                if data == 1:
                    next_state = S11
                else:
                    next_state = S0
            elif state == S11:
                if data == 1:
                    next_state = S11
                else:
                    next_state = S110
            elif state == S110:
                if data == 1:
                    next_state = FOUND
                else:
                    next_state = S0
            elif state == FOUND:
                next_state = FOUND
            else:
                next_state = S0

        # Same-cycle output after the sampled posedge.
        if reset == 1:
            # r_reset_clear
            start_shifting = 0
        else:
            if state == FOUND or (state == S110 and data == 1):
                # r_set_or_hold
                start_shifting = 1
            else:
                # r_default_clear
                start_shifting = 0

        outputs.append({"start_shifting": start_shifting})
        state = next_state

        # Mid changes occur after sampling and are carried to the next row.
        if "mid" in row:
            mid = row["mid"]
            if mid is not None:
                if "reset" in mid:
                    cur_reset = mid["reset"]
                if "data" in mid:
                    cur_data = mid["data"]

    return outputs
