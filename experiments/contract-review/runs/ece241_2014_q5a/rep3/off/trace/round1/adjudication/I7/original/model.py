def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore FSM.
    # States: S0 (copy phase, no 1 seen yet), S1 (invert phase, 1 seen).
    # R3: areset==1 asynchronously forces state=S0 and z=0 (priority 0).
    # R1: state==S0 -> z = x (combinational, same cycle).
    # R2: state==S1 -> z = ~x (combinational, same cycle).
    # R4: posedge clk, areset==0: if state==S0 and x==1 -> next state=S1; else unchanged.

    state = "S0"  # power-up state (unspecified but we choose S0)
    results = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R3: asynchronous reset forces state to S0 and z to 0
        if areset == 1:
            state = "S0"
            z = 0
            results.append({"z": z & 1})
            continue

        # R1 / R2: combinational output based on current state
        if state == "S0":
            z = x  # R1
        else:  # state == "S1"
            z = (~x) & 1  # R2

        results.append({"z": z & 1})

        # R4: posedge clk transition (areset==0)
        if state == "S0" and x == 1:
            state = "S1"
        # else state unchanged

    return results
