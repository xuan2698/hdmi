def reference(vectors):
    # State: q_state holds the registered 8-bit output value.
    # Contract rules:
    # R1_sync_reset: reset == 1 -> q = 0 on posedge clk (priority 1)
    # R2_dff_capture: reset == 0 -> q = d on posedge clk (priority 2)
    # Candidate interpretation for global: reset is asynchronous active-high,
    # clearing q immediately when reset=1 regardless of clock edge.
    q_state = 0  # power-up unspecified; use 0 as concrete value
    out = []
    for row in vectors:
        d = row.get('d', 0)
        reset = row.get('reset', 0)
        # Asynchronous reset: if reset is high, q clears immediately (before edge)
        if reset == 1:
            q_state = 0  # R1_sync_reset (async interpretation)
        # Posedge clk sampling
        if reset == 1:
            q_state = 0  # R1_sync_reset
        else:
            q_state = d & 0xFF  # R2_dff_capture
        out.append({'q': q_state & 0xFF})
    return out
