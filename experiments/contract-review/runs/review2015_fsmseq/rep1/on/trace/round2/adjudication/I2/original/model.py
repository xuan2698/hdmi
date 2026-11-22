def reference(vectors):
    state = "S0"
    start_shifting = 0
    cur_reset = 0
    cur_data = 0
    outputs = []

    for row in vectors:
        # Apply inputs driven before the sampled posedge.
        try:
            inputs = row["inputs"]
            if "reset" in inputs:
                cur_reset = inputs["reset"]
            if "data" in inputs:
                cur_data = inputs["data"]
        except:
            pass

        if "reset" in row:
            cur_reset = row["reset"]
        if "data" in row:
            cur_data = row["data"]

        # Sample at posedge and compute same-cycle visible output.
        if cur_reset == 1:
            # R_RESET: synchronous active-high reset forces S0 and start_shifting=0.
            state = "S0"
            start_shifting = 0
        else:
            if state == "FOUND":
                # R_HOLD_FOUND: once found, stay found forever until reset.
                start_shifting = 1
            elif state == "S110" and cur_data == 1:
                # R_COMPLETE_1101: sequence 1101 completes on this posedge.
                state = "FOUND"
                start_shifting = 1
            else:
                # R_ZERO_NOT_FOUND: before detection, start_shifting remains 0.
                start_shifting = 0
                if state == "S0":
                    if cur_data == 1:
                        state = "S1"
                    else:
                        state = "S0"
                elif state == "S1":
                    if cur_data == 1:
                        state = "S11"
                    else:
                        state = "S0"
                elif state == "S11":
                    if cur_data == 1:
                        state = "S11"
                    else:
                        state = "S110"
                elif state == "S110":
                    if cur_data == 1:
                        state = "FOUND"
                    else:
                        state = "S0"

        outputs.append({"start_shifting": start_shifting})

        # Optional mid input changes occur AFTER sampling and carry to next row.
        try:
            mid = row["mid"]
            try:
                if "reset" in mid:
                    cur_reset = mid["reset"]
            except:
                pass
            try:
                if "data" in mid:
                    cur_data = mid["data"]
            except:
                pass
        except:
            pass

        if "mid_reset" in row:
            cur_reset = row["mid_reset"]
        if "mid_data" in row:
            cur_data = row["mid_data"]
        if "reset_mid" in row:
            cur_reset = row["reset_mid"]
        if "data_mid" in row:
            cur_data = row["data_mid"]

    return outputs
