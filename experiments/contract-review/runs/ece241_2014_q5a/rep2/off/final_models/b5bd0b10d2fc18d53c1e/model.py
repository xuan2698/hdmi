def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore machine.
    # States: S0 (no 1 seen yet), S1 (at least one 1 seen).
    # R4: async reset (areset=1) -> state S0, z forced to 0 (same cycle).
    # R1: in S0, z = x (combinational, same cycle).
    # R2: in S1, z = NOT x (combinational, same cycle).
    # R3: posedge transitions: S0->S1 if x=1 else S0; S1->S1 always.
    # Mid changes occur after sampling, carried to next row.

    state = "S0"  # power-up state (unspecified, choose S0)
    results = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R4: asynchronous reset asserted -> state S0, z=0 same cycle
        if areset == 1:
            state = "S0"
            z = 0
            results.append({"z": z & 1})
            # reset is async; state stays S0. No posedge transition applied.
            continue

        # Combinational output based on current state (R1 / R2)
        if state == "S0":
            z = x & 1  # R1
        else:  # S1
            z = (~x) & 1  # R2

        results.append({"z": z & 1})

        # R3: posedge transition (sampled at this edge, visible next cycle)
        if state == "S0":
            if x == 1:
                state = "S1"
            else:
                state = "S0"
        else:
            state = "S1"

    return results
