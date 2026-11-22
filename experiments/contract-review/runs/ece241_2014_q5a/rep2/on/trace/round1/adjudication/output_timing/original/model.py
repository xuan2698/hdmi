def reference(vectors):
    # Initial state: S0 (no 1 received yet), z=0.
    state = 0
    z = 0
    cur_areset = 0
    cur_x = 0
    out = []

    for row in vectors:
        # Drive each row's inputs before the sampled posedge.
        if "areset" in row:
            cur_areset = row["areset"]
        if "x" in row:
            cur_x = row["x"]

        if cur_areset == 1:
            # async_reset_z0: asynchronously force state S0 and z=0 while reset asserted.
            state = 0
            z = 0
        else:
            # Posedge transitions when areset=0.
            if state == 0:
                if cur_x == 0:
                    # s0_x0: next state S0; z=0 after edge.
                    state = 0
                else:
                    # s0_x1: next state S1; z=1 after edge.
                    state = 1
            elif state == 1:
                if cur_x == 0:
                    # s1_x0: next state S1; z=1 after edge.
                    state = 1
                else:
                    # s1_x1: next state S2; z=0 after edge.
                    state = 2
            else:  # state == 2
                if cur_x == 0:
                    # s2_x0: next state S1; z=1 after edge.
                    state = 1
                else:
                    # s2_x1: next state S2; z=0 after edge.
                    state = 2

            # Moore output after the edge based on the new state.
            if state == 1:
                z = 1
            else:
                z = 0

        # Record the sampled output for this row.
        out.append({"z": z})

        # Process optional mid changes after sampling, before the next clock edge.
        if "mid" in row:
            mid = row["mid"]
            if "areset" in mid:
                cur_areset = mid["areset"]
            if "x" in mid:
                cur_x = mid["x"]

            # async_reset_z0: if mid asserts reset, force S0 and z=0 immediately.
            if cur_areset == 1:
                state = 0
                z = 0

    return out
