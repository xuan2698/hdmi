def reference(vectors):
    # Contract implementation.
    # State: S0 = no 1-bit seen yet (copy phase), S1 = 1-bit seen (invert phase).
    # Reset: async, active high, forces state to S0 and z to 0.
    # Output: combinational, visible same cycle (per resolved interpretation).
    #   R1: state == S0 -> z = x
    #   R2: state == S1 -> z = ~x
    #   R3: areset == 1 -> state = S0, z = 0 (async, same cycle)
    #   R4: posedge clk, areset == 0: if state == S0 and x == 1 -> next state = S1
    # Mid changes occur AFTER sampling, before other edge, carried to next row.

    state = "S0"
    out = []

    for row in vectors:
        areset = row.get("areset", 0) & 1
        x = row.get("x", 0) & 1

        # R3: asynchronous reset forces state to S0 and z to 0 (same cycle)
        if areset == 1:
            state = "S0"
            z = 0
            out.append({"z": z & 1})
            continue

        # Combinational output based on current state (same cycle)
        # R1: state == S0 -> z = x
        # R2: state == S1 -> z = ~x
        if state == "S0":
            z = x
        else:  # S1
            z = (~x) & 1

        out.append({"z": z & 1})

        # R4: posedge clk, areset == 0: state transition
        if state == "S0" and x == 1:
            state = "S1"
        # else state unchanged

    return out
