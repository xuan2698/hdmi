def reference(vectors):
    # State encoding: S0=0, S1=1, S2=2, S3=3, SF=4
    state = 0
    start_shifting = 0
    cur_reset = 0
    cur_data = 0
    result = []

    for row in vectors:
        # Values driven before the sampled posedge.
        if "reset" in row:
            cur_reset = row["reset"]
        if "data" in row:
            cur_data = row["data"]

        if cur_reset == 1:
            # R_RESET: synchronous active-high reset overrides all other rules.
            state = 0
            start_shifting = 0
        elif state == 4:
            # R_HOLD: sequence found; hold start_shifting forever until reset.
            state = 4
            start_shifting = 1
        elif state == 3 and cur_data == 1:
            # R_DETECT: current state S3 and data 1 detects 1101.
            state = 4
            start_shifting = 1
        else:
            # R_PROGRESS: continue searching for 1101.
            if state == 0:
                if cur_data == 1:
                    state = 1
                else:
                    state = 0
            elif state == 1:
                if cur_data == 1:
                    state = 2
                else:
                    state = 0
            elif state == 2:
                if cur_data == 0:
                    state = 3
                else:
                    state = 2
            else:
                state = 0
            start_shifting = 0

        result.append({"start_shifting": start_shifting})

        # Optional mid changes are applied after sampling and persist to next row.
        if "mid" in row:
            mid = row["mid"]
            if mid:
                if "reset" in mid:
                    cur_reset = mid["reset"]
                if "data" in mid:
                    cur_data = mid["data"]

    return result
