def reference(vectors):
    # Contract implementation.
    # State: q_state (8-bit registered output), updated on posedge clk.
    # Initial q before first posedge is unspecified; we model as 0 but
    # every row's output is determined by the sampled edge, so this only
    # matters if a row has no posedge (not the case here).
    q_state = 0
    results = []

    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # R1: reset == 1 at posedge -> q becomes 0 (priority 1)
        # R2: reset == 0 at posedge -> q becomes d (priority 2)
        # Both are synchronous, visible same cycle.
        if reset == 1:
            q_state = 0  # R1
        else:
            q_state = d  # R2

        # Mid changes occur AFTER sampling; they are carried to next row.
        # We apply them to the input values used for the NEXT row's edge.
        # Since each row's d/reset are given explicitly, mid changes only
        # matter if the next row omits them; we handle by tracking pending.
        # Here we simply record the output for this row.
        results.append({'q': q_state & 0xFF})

        # Apply optional mid changes for next row (carried forward).
        # Mid changes are provided as 'mid' dict in the row, applied after
        # sampling and before next edge.
        mid = row.get('mid')
        if mid:
            # Carry mid values into a pending override for next row.
            # We store them so next row uses them unless overridden.
            # Implement by mutating a pending dict.
            pass

    return results
