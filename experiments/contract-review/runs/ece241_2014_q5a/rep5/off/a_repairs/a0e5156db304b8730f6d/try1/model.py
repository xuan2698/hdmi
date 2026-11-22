def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore machine.
    # States: S0 (no 1 seen yet), S1 (a 1 has been seen).
    # R5: async reset forces state to S0 and z=0 immediately.
    # R1: In S0, z = x (combinational, same cycle).
    # R2: In S1, z = NOT x (combinational, same cycle).
    # R3: On posedge, if x=1 -> S1, else stay S0 (from S0).
    # R4: On posedge, once in S1, stay S1 regardless of x.
    # Mid changes occur after sampling, carried to start of next row.

    state = "S0"  # power-up state
    out = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R5: asynchronous reset asserted -> state S0, z=0 immediately
        if areset == 1:
            state = "S0"
            z = 0
            out.append({"z": z & 1})
            # mid changes after sampling: apply to next row's start
            # (mid changes are carried to start of next row; we handle by
            #  reading row values at start of each iteration, so nothing
            #  extra needed here since next row dict already has values)
            continue

        # R1 / R2: combinational output based on current state
        if state == "S0":
            z = x  # R1
        else:
            z = 1 - x  # R2

        out.append({"z": z & 1})

        # R3 / R4: posedge state update (sampled after edge settles)
        if state == "S0":
            if x == 1:
                state = "S1"  # R3
            else:
                state = "S0"  # R3
        else:
            state = "S1"  # R4

    return out
