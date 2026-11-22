def reference(vectors):
    # Contract implementation.
    # State: q_state = 8-bit registered output, updated on posedge clk.
    # R1: reset == 1 at posedge -> q becomes 0 (synchronous, active high).
    # R2: reset == 0 at posedge -> q becomes d (D flip-flop behavior).
    # Power-up unspecified: initialize q_state to 0 (concrete value required).
    q_state = 0
    results = []
    for row in vectors:
        # Sample inputs at the posedge (values driven before the edge).
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1
        # R1: active high synchronous reset takes priority.
        if reset == 1:
            q_state = 0
        else:
            # R2: D flip-flop captures d.
            q_state = d
        # Output visible same cycle after posedge settles.
        results.append({'q': q_state & 0xFF})
        # Mid input changes occur AFTER sampling; they are carried to the
        # start of the next row, so no action needed here (next row's
        # inputs already reflect them).
    return results
