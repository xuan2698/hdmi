def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore FSM.
    # States: S0 = no 1-bit seen yet (pass through), S1 = at least one 1-bit seen (complement).
    # Reset: asynchronous, active high, forces state to S0 and z=0.
    # Outputs are combinational based on current state and current input x.
    # State updates on posedge clk (sampled after edge settles).

    state = "S0"  # power-up state (unspecified, but we choose S0)
    results = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R4: Asynchronous reset asserted -> state forced to S0, z=0 (same cycle)
        if areset == 1:
            state = "S0"
            z = 0
            results.append({"z": z})
            continue

        # Combinational output based on current state and current input x
        if state == "S0":
            # R1: In S0, z = x (pass through until first 1)
            z = x
        else:  # state == "S1"
            # R2: In S1, z = NOT x (complement bits after first 1)
            z = 1 - x

        results.append({"z": z})

        # R3: State transition on posedge clk (visible next cycle)
        # S0 -> S1 when x=1; S1 stays S1
        if state == "S0" and x == 1:
            state = "S1"
        # S1 stays S1 (no change needed)

    return results
