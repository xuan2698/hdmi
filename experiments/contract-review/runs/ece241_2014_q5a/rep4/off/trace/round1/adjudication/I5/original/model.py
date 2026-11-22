def reference(vectors):
    # State machine implementation for 2's complementer (LSB-first)
    # States: S0 (no 1 seen yet), S1 (1 seen, complementing)
    # R4: async reset forces state to S0 and z=0
    # R1: In S0, z = x
    # R2: In S1, z = NOT x
    # R3: posedge transitions: S0->S1 when x=1; S1 stays S1; S0 stays S0 when x=0

    state = "S0"  # power-up state (unspecified, but reset will handle)
    results = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R4: asynchronous reset - state forced to S0, z=0 regardless of clock
        if areset == 1:
            state = "S0"
            z = 0
            results.append({"z": z})
            continue

        # Combinational output based on current state (before posedge update)
        # R1: In state S0: z = x
        # R2: In state S1: z = NOT x
        if state == "S0":
            z = x & 1
        else:  # S1
            z = (~x) & 1

        results.append({"z": z})

        # R3: posedge state transition (sampled at posedge, visible next cycle)
        # S0 -> S1 when x=1; S1 stays S1; S0 stays S0 when x=0
        if state == "S0":
            if x == 1:
                state = "S1"
            # else stays S0
        # S1 stays S1

    return results
