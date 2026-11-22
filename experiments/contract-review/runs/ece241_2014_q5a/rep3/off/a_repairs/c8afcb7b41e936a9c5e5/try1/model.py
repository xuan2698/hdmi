def reference(vectors):
    # Contract implementation.
    # State: S0 = no 1-bit seen yet (copy phase), S1 = 1-bit seen (invert phase).
    # Moore machine: z is registered on posedge clk, visible next cycle.
    # Asynchronous active-high reset forces state to S0 and z to 0.

    state = "S0"
    z = 0
    out = []

    for row in vectors:
        areset = row["areset"]
        x = row["x"]

        # R3: asynchronous reset forces state to S0 and z to 0 (same cycle).
        if areset == 1:
            state = "S0"
            z = 0
            out.append({"z": z})
            continue

        # R1/R2: Moore output based on current state, visible next cycle.
        # Compute output from current state (registered output).
        if state == "S0":
            # R1: state == S0: z = x
            z = x
        else:
            # R2: state == S1: z = ~x
            z = 1 - x

        # R4: posedge clk, areset == 0: state transition.
        if state == "S0" and x == 1:
            state = "S1"
        # else state unchanged

        out.append({"z": z})

    return out
