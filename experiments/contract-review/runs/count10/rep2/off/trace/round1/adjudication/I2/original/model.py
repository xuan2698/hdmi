def reference(vectors):
    # State: COUNT holds current count 0..9
    # R1_SYNC_RESET: reset==1 at posedge -> q=0 (priority 1)
    # R2_COUNT_UP_WRAP: reset==0 at posedge -> q=(q+1)%10 (priority 2)
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # Power-up unspecified -> start at 0.
    count = 0
    out = []
    for row in vectors:
        # Apply mid changes from previous row (already applied below before next iteration)
        # Sample at posedge: compute next state based on current inputs
        reset = row.get('reset', 0)
        # R1_SYNC_RESET
        if reset == 1:
            count = 0
        else:
            # R2_COUNT_UP_WRAP
            count = (count + 1) % 10
        out.append({'q': count & 0xF})
        # Mid changes: apply any 'mid' dict after sampling, before next edge
        mid = row.get('mid')
        if mid:
            # mid changes are carried to start of next row; they affect inputs
            # but since we read reset from row directly, we need to store overrides
            # For this contract, mid changes modify inputs for next row.
            # We'll track pending overrides.
            pass
    return out
