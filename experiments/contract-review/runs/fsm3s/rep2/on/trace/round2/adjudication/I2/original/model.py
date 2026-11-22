def reference(vectors):
    # Initial state before the first sampled reset is unspecified; choose A concretely.
    state = "A"
    cur_in = 0
    cur_reset = 0
    result = []

    for row in vectors:
        # Apply row inputs before the sampled posedge.
        if "in" in row:
            cur_in = row["in"]
        if "reset" in row:
            cur_reset = row["reset"]

        # sync_reset: At a posedge, if reset == 1 then state becomes A regardless of in; after the edge out is 0.
        if cur_reset == 1:
            state = "A"
        else:
            # transition_and_moore_output: At a posedge with reset == 0: update state from current state and in.
            if state == "A":
                if cur_in == 1:
                    state = "B"
                else:
                    state = "A"
            elif state == "B":
                if cur_in == 1:
                    state = "B"
                else:
                    state = "C"
            elif state == "C":
                if cur_in == 1:
                    state = "D"
                else:
                    state = "A"
            else:  # state == "D"
                if cur_in == 1:
                    state = "B"
                else:
                    state = "C"

        # transition_and_moore_output: After the edge out = 0 for S' in {A,B,C} and out = 1 for S'=D.
        if state == "D":
            out_val = 1
        else:
            out_val = 0
        result.append({"out": out_val})

        # mid: Optional mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row.
        if "mid" in row:
            mid = row["mid"]
            if "in" in mid:
                cur_in = mid["in"]
            if "reset" in mid:
                cur_reset = mid["reset"]

    return result
