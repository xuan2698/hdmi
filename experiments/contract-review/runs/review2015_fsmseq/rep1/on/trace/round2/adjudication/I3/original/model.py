def reference(vectors):
    # FSM states: S0, S1, S11, S110, FOUND
    state = "S0"
    inputs = {"reset": 0, "data": 0}
    results = []
    for row in vectors:
        # Drive row inputs before sampled posedge
        if "reset" in row:
            inputs["reset"] = row["reset"]
        if "data" in row:
            inputs["data"] = row["data"]
        reset = inputs["reset"]
        data = inputs["data"]

        # Determine next state at posedge
        if reset == 1:
            # R_RESET: active high synchronous reset forces S0
            next_state = "S0"
        else:
            if state == "S0":
                next_state = "S1" if data == 1 else "S0"
            elif state == "S1":
                next_state = "S11" if data == 1 else "S0"
            elif state == "S11":
                next_state = "S11" if data == 1 else "S110"
            elif state == "S110":
                if data == 1:
                    # R_COMPLETE_1101: sequence 1101 completed
                    next_state = "FOUND"
                else:
                    next_state = "S0"
            elif state == "FOUND":
                # R_HOLD_FOUND: stay found forever until reset
                next_state = "FOUND"
            else:
                next_state = "S0"
        state = next_state

        # R_ZERO_NOT_FOUND: start_shifting is 0 unless FOUND.
        # Output is visible same cycle (post-posedge) as state update.
        start_shifting = 1 if state == "FOUND" else 0
        results.append({"start_shifting": start_shifting})

        # Process optional mid input changes AFTER sampling, carried to next row
        if "mid" in row:
            mid = row["mid"]
            for k in mid:
                if k in inputs:
                    inputs[k] = mid[k]
        for k in row:
            if k.endswith("_mid"):
                base = k[:-4]
                if base in inputs:
                    inputs[base] = row[k]
    return results
