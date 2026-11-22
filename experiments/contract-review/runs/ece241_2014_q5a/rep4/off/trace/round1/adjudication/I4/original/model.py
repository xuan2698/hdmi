def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore machine.
    # States: S0 (no 1 seen yet), S1 (a 1 has been seen; complementing).
    # Outputs are combinational functions of state and x (Mealy-like output
    # but state is Moore; per contract R1/R2 output depends on x too).
    # R4: async reset forces state S0 and z=0.
    # R3: posedge transition S0->S1 when x=1; S1 stays S1; S0 stays S0 when x=0.
    # R1: In S0, z = x.
    # R2: In S1, z = NOT x.
    # mid changes occur after sampling edge, carried to next row.

    state = "S0"  # power-up unspecified but reset forces S0; start at S0
    results = []

    for row in vectors:
        areset = row.get("areset", 0) & 1
        x = row.get("x", 0) & 1

        # R4: asynchronous reset asserted -> state forced S0, z=0
        if areset == 1:
            state = "S0"
            z = 0
            results.append({"z": z & 1})
            # mid changes after sampling: apply to state for next row
            mid = row.get("mid")
            if mid is not None:
                # mid changes are input changes after sampling; they affect
                # next row's sampled values, not state directly here.
                pass
            continue

        # Combinational output based on current state and x
        if state == "S0":
            # R1: z = x
            z = x
        else:  # S1
            # R2: z = NOT x
            z = 1 - x

        results.append({"z": z & 1})

        # R3: posedge state transition (sampled at this edge)
        if state == "S0":
            if x == 1:
                state = "S1"
            # else stay S0
        # S1 stays S1

        # mid changes occur after sampling edge; carried to start of next row.
        # They do not affect current row's sampled values or state update here
        # (state update already done based on sampled x). Mid changes would
        # affect next row's x/areset values, which are provided in next row.

    return results
