def reference(vectors):
    # Contract implementation.
    # State: q_reg (8-bit), power-up unspecified -> concrete 0.
    # R1_sync_reset: on posedge clk, if reset==1, q <= 0 (priority 1).
    # R2_dff_capture: on posedge clk, if reset==0, q <= d (priority 2).
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # Candidate interpretation for unresolved field: on posedge with reset=1,
    # q captures d instead of clearing. Apply this candidate interpretation.
    q_reg = 0  # named state, concrete power-up value
    out = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1
        # Sample at posedge: apply candidate interpretation (reset=1 -> capture d)
        # R1_sync_reset (candidate override): reset==1 -> q <= d
        # R2_dff_capture: reset==0 -> q <= d
        # Both branches capture d under candidate interpretation.
        q_reg = d & 0xFF
        out.append({'q': q_reg})
    return out
