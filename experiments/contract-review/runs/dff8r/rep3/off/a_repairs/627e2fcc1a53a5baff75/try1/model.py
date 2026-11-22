def reference(vectors):
    # Contract implementation for 8 D flip-flops with active-high synchronous reset.
    # State: q_state (8-bit registered output), updated on posedge clk.
    # R1: reset == 1 at posedge -> q becomes 0 (priority 1).
    # R2: reset == 0 at posedge -> q becomes d (priority 2).
    # Timing: each row's inputs are driven before the sampled posedge.
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.
    # Power-up state is unspecified; we choose 0 as a concrete initial value.

    q_state = 0  # R2: initial registered value (concrete, power-up unspecified)
    results = []

    for row in vectors:
        d = row.get('d', 0)
        reset = row.get('reset', 0)

        # Sample at posedge clk: compute next state from current inputs.
        if reset == 1:
            # R1: active high synchronous reset -> q = 0
            q_state = 0
        else:
            # R2: D flip-flop -> q = d
            q_state = d & 0xFF

        # Output visible same cycle after edge settles.
        results.append({'q': q_state & 0xFF})

    return results
