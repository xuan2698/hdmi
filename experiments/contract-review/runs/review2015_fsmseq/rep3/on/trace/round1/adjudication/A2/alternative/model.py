def reference(vectors):
    # State encoding
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4
    state = S0
    start_shifting = 0
    reset_seen = 0
    current_inputs = {}
    outputs = []

    for row in vectors:
        # Drive pre-edge values for this row
        for key in ("reset", "data"):
            if key in row:
                current_inputs[key] = row[key]

        r = current_inputs.get("reset", 0)
        d = current_inputs.get("data", 0)

        if r == 1:
            # R1_reset_clear: synchronous active-high reset has priority
            state = S0
            start_shifting = 0
            reset_seen = 1  # mark that a reset has occurred
        else:
            # reset == 0: compute next state following the 1101 prefix transitions
            if state == S0:
                next_state = S1 if d == 1 else S0
            elif state == S1:
                next_state = S2 if d == 1 else S0
            elif state == S2:
                next_state = S3 if d == 0 else S2
            elif state == S3:
                next_state = S4 if d == 1 else S0
            elif state == S4:
                next_state = S4
            else:
                next_state = S0

            # R2_detect_set_and_hold: detection sets start_shifting=1 and holds in S4
            detected = (state == S4) or (state == S3 and d == 1)

            # R3_default_zero_while_searching, with candidate interpretation:
            # after reset releases, start_shifting is 1 until 1101 is detected,
            # while reset clears it to 0.
            if reset_seen == 1:
                start_shifting = 1
            else:
                start_shifting = 1 if detected else 0

            state = next_state

        # Output visible after the posedge
        outputs.append({"start_shifting": start_shifting})

        # Process optional mid changes after sampling, carried to next row's inputs
        if "mid" in row:
            for key, val in row["mid"].items():
                current_inputs[key] = val

    return outputs
