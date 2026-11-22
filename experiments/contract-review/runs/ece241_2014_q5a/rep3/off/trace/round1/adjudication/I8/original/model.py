def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore FSM.
    # States: S0 = copy phase (no 1 seen yet), S1 = invert phase (1 seen).
    # Inputs: areset (async active-high reset), x (serial LSB-first bit).
    # Output: z (combinational per state and x).
    #
    # R3: areset == 1 asynchronously forces state to S0 and z to 0.
    # R1: state == S0 -> z = x (same cycle, combinational).
    # R2: state == S1 -> z = ~x (same cycle, combinational).
    # R4: posedge clk, areset == 0: if state == S0 and x == 1 -> next state = S1;
    #     else state unchanged. Visible next cycle.

    state = "S0"  # power-up state (unspecified, but S0 is a safe concrete choice)
    out = []

    for row in vectors:
        areset = row.get("areset", 0) & 1
        x = row.get("x", 0) & 1

        # R3: asynchronous reset forces state to S0 and z to 0 (same cycle).
        if areset == 1:
            state = "S0"
            z = 0
            out.append({"z": z & 1})
            # mid changes are carried to next row; no state update on reset
            continue

        # R1 / R2: combinational output based on current state and x.
        if state == "S0":
            z = x  # R1
        else:  # state == "S1"
            z = (~x) & 1  # R2

        out.append({"z": z & 1})

        # R4: posedge clk state update (visible next cycle).
        if state == "S0" and x == 1:
            state = "S1"
        # else state unchanged

    return out
