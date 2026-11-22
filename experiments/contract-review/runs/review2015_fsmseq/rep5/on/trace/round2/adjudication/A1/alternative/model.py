def reference(vectors):
    # State encoding
    S0 = 0
    S1 = 1
    S11 = 2
    S110 = 3
    FOUND = 4

    state = S0
    current_reset = 0
    current_data = 0
    result = []

    for row in vectors:
        # Drive row inputs before the sampled posedge.
        if "reset" in row:
            current_reset = row["reset"] & 1
        if "data" in row:
            current_data = row["data"] & 1

        reset = current_reset
        data = current_data

        # R_RESET_CLEAR: synchronous active-high reset clears output to 0.
        # R_KEEP_ZERO_UNTIL_FOUND: before FOUND, output stays 0 (next_cycle delay included).
        # R_SET_OR_HOLD_1101 (next_cycle): output is 1 only after the posedge following entry to FOUND.
        if reset == 1:
            out = 0
        else:
            if state == FOUND:
                out = 1
            else:
                out = 0

        # State transition after sampled posedge; reset has priority.
        if reset == 1:
            state = S0  # R_RESET_CLEAR
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
                    state = FOUND  # Detection; output becomes 1 on following posedge due to next_cycle.
                else:
                    state = S0
            else:  # FOUND
                state = FOUND  # R_SET_OR_HOLD_1101 hold

        result.append({"start_shifting": out})

        # Optional mid input changes occur after sampling, before the other edge,
        # and are carried to the start of the next row.
        if "mid" in row:
            mid = row["mid"]
            if mid:
                try:
                    # mid as a mapping of input name to value
                    for key in mid:
                        val = mid[key]
                        if key == "reset":
                            current_reset = val & 1
                        elif key == "data":
                            current_data = val & 1
                except:
                    # mid as a sequence of mappings
                    for change in mid:
                        for key in change:
                            val = change[key]
                            if key == "reset":
                                current_reset = val & 1
                            elif key == "data":
                                current_data = val & 1

    return result
