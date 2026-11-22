def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore machine.
    # States: S0 (no 1 seen yet), S1 (at least one 1 seen).
    # Outputs are combinational based on current state and x (same cycle).
    # State updates on posedge clk. Asynchronous active-high reset forces S0 and z=0.

    # State encoding
    S0 = 0
    S1 = 1

    state = S0  # power-up state (unspecified, but we pick S0)
    results = []

    for vec in vectors:
        areset = vec.get('areset', 0) & 1
        x = vec.get('x', 0) & 1

        # R4: Asynchronous reset asserted -> state forced to S0, z=0 (same cycle)
        if areset:
            state = S0
            z = 0
            results.append({'z': z})
            continue

        # R1 / R2: combinational output based on current state and x (same cycle)
        if state == S0:
            # R1: In S0, z = x
            z = x
        else:
            # R2: In S1, z = NOT x
            z = 1 - x

        results.append({'z': z})

        # R3: State transition on posedge clk (visible next cycle)
        # S0 -> S1 when x=1; S1 stays S1; S0 stays S0 when x=0
        if state == S0 and x == 1:
            state = S1
        # else state unchanged

    return results
