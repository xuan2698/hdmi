def reference(vectors):
    # Contract implementation.
    # State: q_state (8-bit registered output), updated on posedge clk.
    # R1: reset == 1 at posedge -> q becomes 0 (priority 1).
    # R2: reset == 0 at posedge -> q becomes d sampled at that edge (priority 2).
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.
    # Power-up unspecified: use 0 as concrete initial value.

    q_state = 0  # R2 (initial concrete value; power-up unspecified)
    out = []

    for row in vectors:
        d = row.get('d', 0)
        reset = row.get('reset', 0)

        # Sample at posedge: apply rules with priority.
        if reset == 1:
            # R1: active high synchronous reset
            q_state = 0
        else:
            # R2: D flip-flop captures d at posedge
            q_state = d & 0xFF

        # Output visible same cycle after posedge settles.
        out.append({'q': q_state & 0xFF})

        # Mid changes (if any) occur AFTER sampling; they affect next row's inputs.
        # Since inputs are provided per-row already, nothing extra to do here.

    return out
