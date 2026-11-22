def reference(vectors):
    # Active-high asynchronous reset; Moore states A/B/C; output z is 1 bit.
    state = "A"
    z = 0
    cur_areset = 0
    cur_x = 0
    result = []

    for row in vectors:
        # Inputs driven before the sampled posedge; carried mid values are defaults.
        if "areset" in row:
            cur_areset = int(row["areset"])
        if "x" in row:
            cur_x = int(row["x"])

        if cur_areset == 1:
            # async_reset_assert: asynchronous active-high reset forces state A, z=0.
            state = "A"
            z = 0
        else:
            # Posedge transition when reset is inactive.
            if state == "A":
                if cur_x == 0:
                    # A_on_x0: remain in A, z=0.
                    state = "A"
                    z = 0
                else:
                    # A_on_x1: go to B, z=1.
                    state = "B"
                    z = 1
            elif state == "B":
                if cur_x == 0:
                    # B_on_x0: remain in B, z=1.
                    state = "B"
                    z = 1
                else:
                    # B_on_x1: go to C, z=0.
                    state = "C"
                    z = 0
            else:
                if cur_x == 0:
                    # C_on_x0: go to B, z=1.
                    state = "B"
                    z = 1
                else:
                    # C_on_x1: remain in C, z=0.
                    state = "C"
                    z = 0

        result.append({"z": int(z) & 1})

        # mid changes occur AFTER sampling and are carried into the next row.
        if "mid" in row and row["mid"] is not None:
            mid = row["mid"]
            if "areset" in mid:
                cur_areset = int(mid["areset"])
                if cur_areset == 1:
                    # async_reset_assert: mid-cycle reset assertion also takes effect asynchronously.
                    state = "A"
                    z = 0
            if "x" in mid:
                cur_x = int(mid["x"])

    return result
