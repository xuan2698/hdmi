def reference(vectors):
    # Contract implementation.
    # State: S0 = no 1-bit seen yet (copy phase), S1 = 1-bit seen (invert phase).
    # R3: areset==1 asynchronously forces state to S0 and z to 0 (priority 0).
    # R1: state==S0 -> z = x (combinational, same cycle).
    # R2: state==S1 -> z = ~x (combinational, same cycle).
    # R4: posedge clk, areset==0: if state==S0 and x==1 -> next state S1; else unchanged.
    # Mid changes occur AFTER sampling, before other edge, carried to next row.

    state = "S0"
    out = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R3: asynchronous reset forces state S0 and z=0 (priority 0)
        if areset == 1:
            state = "S0"
            z = 0
            out.append({"z": z & 1})
            # mid changes carried to next row (already reflected in next row's dict)
            continue

        # R1 / R2: combinational output based on current state
        if state == "S0":
            z = x & 1  # R1
        else:
            z = (~x) & 1  # R2

        out.append({"z": z & 1})

        # R4: posedge clk update (areset==0)
        if state == "S0" and x == 1:
            state = "S1"
        # else state unchanged

    return out
