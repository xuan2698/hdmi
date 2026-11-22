def reference(vectors):
    # State machine: S0 = copy phase, S1 = invert phase
    # R3: async reset forces state S0 and z=0
    # R1: state S0 -> z = x
    # R2: state S1 -> z = ~x
    # R4: posedge clk, areset==0: if S0 and x==1 -> S1; else unchanged

    state = "S0"
    out = []

    for row in vectors:
        areset = row["areset"]
        x = row["x"]

        # R3: asynchronous reset forces state to S0 and z to 0 (same cycle)
        if areset == 1:
            state = "S0"
            z = 0  # R3
        else:
            # R1 / R2: combinational output based on current state
            if state == "S0":
                z = x  # R1
            else:
                z = 1 - x  # R2 (bitwise NOT for 1-bit)

        out.append({"z": z})

        # R4: posedge clk update (only when not in reset)
        if areset == 0:
            if state == "S0" and x == 1:
                state = "S1"  # R4
            # else state unchanged

    return out
