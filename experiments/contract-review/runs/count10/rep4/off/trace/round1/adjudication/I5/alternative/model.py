def reference(vectors):
    # Contract implementation.
    # State: COUNT (current decade count 0..9), updated at posedge clk.
    # R1: reset == 1 at posedge -> q becomes 0 (synchronous, registered).
    # R2: reset == 0 && q < 9 at posedge -> q becomes q + 1.
    # R3: reset == 0 && q == 9 at posedge -> q becomes 0.
    # Outputs are registered: sampled value reflects state after the posedge.
    # Power-up state is unspecified; we start at 0 for concreteness.
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.

    q = 0  # COUNT state, concrete initial value (power-up unspecified -> 0)
    out = []

    for row in vectors:
        reset = row.get("reset", 0) & 1  # 1-bit input

        # Sample at posedge: compute next state from current state and inputs.
        # R1: synchronous active-high reset has priority.
        if reset == 1:
            q_next = 0
        # R2: count up while below 9.
        elif q < 9:
            q_next = q + 1
        # R3: wrap from 9 to 0.
        else:
            q_next = 0

        q = q_next  # register update at posedge

        # Output visible same cycle after the edge.
        out.append({"q": q & 0xF})

        # Mid changes (if any) occur after sampling; they affect the next row's
        # inputs, which are already provided by the next vector. Nothing to do.

    return out
