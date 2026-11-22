def reference(vectors):
    # Rule R_RESET / candidate interpretation: reset restarts the detector;
    # start_shifting holds during reset and clears on first posedge reset==0.
    S0 = 0
    S1 = 1
    S11 = 2
    S110 = 3
    FOUND = 4

    state = S0
    start_shifting = 0
    cur_reset = 0
    cur_data = 0
    prev_sampled_reset = 0
    result = []

    for v in vectors:
        # Row values are driven before the sampled posedge.
        if "reset" in v:
            cur_reset = v["reset"]
        if "data" in v:
            cur_data = v["data"]

        reset = cur_reset
        data = cur_data

        # Sampled posedge update.
        if reset == 1:
            # R_RESET: force state S0, hold start_shifting.
            next_state = S0
            next_start = start_shifting
        else:
            # Explicit FSM transitions.
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
                    next_state = FOUND  # R_COMPLETE_1101
                else:
                    next_state = S0
            else:  # FOUND
                next_state = FOUND      # R_HOLD_FOUND

            # Output update.
            if prev_sampled_reset == 1:
                # First posedge with reset==0 after reset high: clear.
                next_start = 0
            else:
                if next_state == FOUND:
                    next_start = 1      # R_COMPLETE_1101 / R_HOLD_FOUND
                else:
                    next_start = 0      # R_ZERO_NOT_FOUND

        # Commit sampled update.
        state = next_state
        start_shifting = next_start
        prev_sampled_reset = reset
        result.append({"start_shifting": start_shifting})

        # Mid changes occur after sampling, before the other edge,
        # and are carried to the start of the next row.
        if "mid" in v:
            mid = v["mid"]
            try:
                if "reset" in mid:
                    cur_reset = mid["reset"]
                if "data" in mid:
                    cur_data = mid["data"]
            except:
                pass

        # Also accept suffixed mid-change keys such as reset_mid/data_mid.
        for k in v:
            if k == "mid":
                continue
            if k.endswith("_mid"):
                sig = k[:-4]
                if sig == "reset":
                    cur_reset = v[k]
                elif sig == "data":
                    cur_data = v[k]

    return result
