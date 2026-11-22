def reference(vectors):
    # Named states for the 1101 sequence detector.
    S0 = 0  # initial/reset: no matching prefix
    S1 = 1  # suffix "1"
    S2 = 2  # suffix "11"
    S3 = 3  # suffix "110"
    S4 = 4  # found 1101; start_shifting latched at 1

    state = S0
    # Concrete power-up input values (chosen 0 for unspecified inputs).
    cur = {"reset": 0, "data": 0}
    result = []

    for row in vectors:
        # Each row's non-mid values are driven before the sampled posedge.
        if "reset" in row:
            cur["reset"] = int(row["reset"])
        if "data" in row:
            cur["data"] = int(row["data"])

        reset_val = cur["reset"] & 1
        data_val = cur["data"] & 1

        # Rule R1_reset_clear: synchronous active-high reset has priority.
        if reset_val == 1:
            next_state = S0
        else:
            # Rule R2_detect_set_and_hold and R3_default_zero_while_searching.
            if state == S0:
                next_state = S1 if data_val == 1 else S0
            elif state == S1:
                next_state = S2 if data_val == 1 else S0
            elif state == S2:
                next_state = S3 if data_val == 0 else S2
            elif state == S3:
                if data_val == 1:
                    # Rule R2_detect_set_and_hold: sequence 1101 found.
                    next_state = S4
                else:
                    next_state = S0
            else:  # state == S4
                # Rule R2_detect_set_and_hold: hold until reset.
                next_state = S4

        # Output after the edge: 1 only in S4; reset forces S0 so output 0.
        start_shifting = 1 if next_state == S4 else 0
        result.append({"start_shifting": start_shifting})

        state = next_state

        # Optional mid changes occur after sampling and are carried forward.
        if "mid" in row:
            mid = row["mid"]
            if "reset" in mid:
                cur["reset"] = int(mid["reset"])
            if "data" in mid:
                cur["data"] = int(mid["data"])

    return result
