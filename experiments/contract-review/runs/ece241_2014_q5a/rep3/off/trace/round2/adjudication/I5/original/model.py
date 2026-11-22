def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore FSM.
    #
    # State meaning:
    #   S0: no 1-bit seen yet (copy phase)  -> z = x
    #   S1: a 1-bit has been seen (invert)  -> z = ~x
    #
    # Timing:
    #   - areset is asynchronous, active high: forces state=S0 and z=0 same cycle (R3)
    #   - On posedge clk with areset==0:
    #       * output z is registered (Moore, next-cycle visible) based on current state (R1/R2)
    #       * state transitions: S0 -> S1 if x==1, else stay; S1 stays (R4)
    #   - Mid input changes occur AFTER sampling, before the other edge, and are
    #     carried to the start of the next row.
    #
    # The vectors list contains rows; each row is a dict with 'areset' and 'x'.
    # Each row's values are driven before the sampled edge. We sample at the
    # posedge (after settling), then apply any mid changes for the next row.

    state = "S0"   # power-up state (unspecified in spec; S0 chosen as reset state)
    z_reg = 0      # registered output

    results = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R3: asynchronous reset forces state to S0 and z to 0 (same cycle)
        if areset == 1:
            state = "S0"
            z_reg = 0
            results.append({"z": z_reg & 1})
            # mid changes (if any) would be applied here; none in this contract
            continue

        # areset == 0: sample at posedge clk
        # R1 / R2: Moore output based on current state (registered, next-cycle visible)
        if state == "S0":
            # R1: z = x
            z_reg = x & 1
        else:  # state == "S1"
            # R2: z = ~x
            z_reg = (~x) & 1

        # R4: state transition on posedge clk
        if state == "S0" and x == 1:
            state = "S1"
        # else state unchanged

        results.append({"z": z_reg & 1})

    return results
