def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore machine.
    # States: S0 (no 1-bit seen yet), S1 (a 1-bit has been seen).
    # Inputs: areset (async, active high), x. Output: z.
    # R4: async reset forces state to S0. Candidate interpretation for
    #     unresolved field: during areset=1, z retains previous value
    #     instead of being forced to 0. We implement the candidate
    #     interpretation (z retains previous value during reset).
    # R1: In S0, z = x (combinational, same cycle).
    # R2: In S1, z = NOT x (combinational, same cycle).
    # R3: posedge transition: S0->S1 when x=1; S1 stays S1; S0 stays S0 when x=0.
    # Mid changes occur after sampling edge, carried to start of next row.

    state = "S0"  # power-up state
    z_prev = 0    # previous z value (for reset retention interpretation)

    results = []
    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R4 (candidate interpretation): during areset=1, z retains previous value.
        # State is forced to S0 asynchronously.
        if areset == 1:
            state = "S0"
            z = z_prev  # retain previous value per candidate interpretation
            results.append({"z": z & 1})
            z_prev = z & 1
            # Mid changes after sampling: none affect state here since reset holds S0.
            continue

        # Combinational output based on current state and x (R1, R2).
        if state == "S0":
            # R1: z = x
            z = x & 1
        else:  # S1
            # R2: z = NOT x
            z = (~x) & 1

        results.append({"z": z})
        z_prev = z

        # R3: posedge state transition (sampled at this edge).
        if state == "S0":
            if x == 1:
                state = "S1"
            # else stay S0
        # S1 stays S1

    return results
