def reference(vectors):
    # State machine implementation for 2's complementer (LSB first)
    # States: S0 = no 1 seen yet, S1 = at least one 1 seen
    # R4: async reset forces state to S0 and z=0 (candidate interpretation overrides:
    #     during async reset, hold last output value instead of forcing z=0)
    # R1: In S0, z = x
    # R2: In S1, z = NOT x
    # R3: S0 -> S1 when x=1; S1 stays S1; state updates on posedge clk

    state = "S0"          # current state
    z_out = 0             # current output value (held during reset per candidate interpretation)
    results = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R4 (candidate interpretation): during async reset, hold last output value.
        # State is forced to S0 asynchronously.
        if areset == 1:
            state = "S0"
            # z_out is held (not forced to 0) per candidate interpretation
            results.append({"z": z_out & 1})
            continue

        # Combinational output based on current state (R1 / R2)
        if state == "S0":
            # R1: In state S0: z = x
            z_out = x & 1
        else:  # S1
            # R2: In state S1: z = NOT x
            z_out = (~x) & 1

        results.append({"z": z_out})

        # R3: State transition on posedge clk (sampled after edge settles)
        if state == "S0" and x == 1:
            state = "S1"
        # S1 stays S1

    return results
