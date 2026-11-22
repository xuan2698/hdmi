def reference(vectors):
    # R_RESET: active-high synchronous reset, sampled at posedge.
    # R_DETECT: candidate interpretation: start_shifting asserts one clock
    #           after the posedge that samples the final 1 of 1101.
    # R_HOLD: once in SF, hold state SF and output 1 while reset=0.
    # R_PROGRESS: search-transition rules for S0/S1/S2/S3.
    state = "S0"
    start_shifting = 0
    cur_reset = 0
    cur_data = 0
    out = []

    for row in vectors:
        # Row inputs are driven before the sampled posedge.
        if "reset" in row:
            cur_reset = row["reset"]
        if "data" in row:
            cur_data = row["data"]

        # R_RESET: reset overrides all other rules at the sampled posedge.
        if cur_reset == 1:
            state = "S0"
            start_shifting = 0
        else:
            if state == "SF":
                # R_HOLD: hold and assert output (delayed by one cycle after detection).
                state = "SF"
                start_shifting = 1
            elif state == "S3" and cur_data == 1:
                # R_DETECT: final 1 sampled; enter SF now, but output asserts next clock.
                state = "SF"
                start_shifting = 0
            else:
                # R_PROGRESS: normal search transitions.
                start_shifting = 0
                if state == "S0":
                    state = "S1" if cur_data == 1 else "S0"
                elif state == "S1":
                    state = "S2" if cur_data == 1 else "S0"
                elif state == "S2":
                    state = "S2" if cur_data == 1 else "S3"
                elif state == "S3":
                    # S3 with data==1 is handled by R_DETECT above.
                    state = "S0"
                else:
                    state = "S0"

        # Optional mid changes occur after sampling and persist to the next row.
        if "mid" in row:
            mid = row["mid"]
            if "reset" in mid:
                cur_reset = mid["reset"]
            if "data" in mid:
                cur_data = mid["data"]

        out.append({"start_shifting": start_shifting})

    return out
