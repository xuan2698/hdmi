def reference(vectors):
    S0 = 0
    S1 = 1
    S11 = 2
    S110 = 3
    FOUND = 4
    state = S0
    out = []
    cur_reset = 0
    cur_data = 0
    for row in vectors:
        # Drive row values before sampled posedge
        if "reset" in row:
            cur_reset = row["reset"]
        if "data" in row:
            cur_data = row["data"]

        reset = cur_reset
        data = cur_data

        if reset == 1:
            # R_RESET: reset forces S0 and start_shifting=0 synchronously
            state = S0
            start_shifting = 0
        else:
            if state == S0:
                if data == 1:
                    state = S1
                else:
                    state = S0
            elif state == S1:
                if data == 1:
                    state = S11
                else:
                    state = S0
            elif state == S11:
                if data == 1:
                    state = S11
                else:
                    state = S110
            elif state == S110:
                if data == 1:
                    # R_COMPLETE_1101: completion sets start_shifting=1 same cycle
                    state = FOUND
                else:
                    state = S0
            else:
                # R_HOLD_FOUND: stay found forever until reset
                state = FOUND

            if state == FOUND:
                start_shifting = 1
            else:
                # R_ZERO_NOT_FOUND: start_shifting is 0 before detection
                start_shifting = 0

        out.append({"start_shifting": start_shifting})

        # Optional mid input changes occur after sampling and carry to next row
        if "mid" in row:
            mid = row["mid"]
            if mid is not None:
                if "reset" in mid:
                    cur_reset = mid["reset"]
                if "data" in mid:
                    cur_data = mid["data"]

    return out
