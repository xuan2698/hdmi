def reference(vectors):
    # Named FSM states: S0, S1, S11, S110, FOUND.
    state = "S0"
    start_shifting = 0
    cur_reset = 0
    cur_data = 0
    result = []

    for row in vectors:
        # Pre-edge input drives for this row.
        if "reset" in row:
            cur_reset = row["reset"]
        if "data" in row:
            cur_data = row["data"]

        reset = cur_reset
        data = cur_data

        if reset == 1:
            # r_reset_clear: synchronous active-high reset has priority.
            # r_reset_clear: reset == 1 forces state S0 and start_shifting 0.
            state = "S0"
            start_shifting = 0
        else:
            # r_set_or_hold: set/hold when FOUND, or when S110 samples final 1.
            if state == "FOUND" or (state == "S110" and data == 1):
                start_shifting = 1
            else:
                # r_default_clear: not found and not completing 1101 on this edge.
                start_shifting = 0

            # Explicit named-state transitions at the sampled posedge.
            if state == "S0":
                if data == 1:
                    state = "S1"
                else:
                    state = "S0"
            elif state == "S1":
                if data == 1:
                    state = "S11"
                else:
                    state = "S0"
            elif state == "S11":
                if data == 1:
                    state = "S11"
                else:
                    state = "S110"
            elif state == "S110":
                if data == 1:
                    state = "FOUND"
                else:
                    state = "S0"
            elif state == "FOUND":
                state = "FOUND"
            else:
                state = "S0"

        result.append({"start_shifting": int(start_shifting)})

        # Optional mid changes occur after this sampled posedge and are carried
        # to the start of the next row's pre-edge inputs.
        mid = row.get("mid", {})
        if mid:
            if "reset" in mid:
                cur_reset = mid["reset"]
            if "data" in mid:
                cur_data = mid["data"]

    return result
