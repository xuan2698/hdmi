def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore machine.
    # States: S0 = no 1 seen yet (pass through), S1 = 1 seen (complement).
    # Reset is asynchronous, active high, forces state S0 and z=0.
    # Outputs are combinational based on current state and current x.
    # State updates on posedge clk (sampled after edge settles).

    results = []
    state = "S0"  # power-up state (unspecified, but we choose S0)

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R4: asynchronous reset asserted -> state forced to S0, z=0
        if areset == 1:
            state = "S0"
            z = 0
            results.append({"z": z})
            continue

        # Combinational output based on current state and x
        # R1: In S0, z = x
        # R2: In S1, z = NOT x
        if state == "S0":
            z = x & 1
        else:  # S1
            z = (~x) & 1

        results.append({"z": z})

        # R3: State transition on posedge clk
        # S0 -> S1 when x=1; S1 stays S1
        if state == "S0" and x == 1:
            state = "S1"
        # S1 stays S1 (no change needed)

    return results
