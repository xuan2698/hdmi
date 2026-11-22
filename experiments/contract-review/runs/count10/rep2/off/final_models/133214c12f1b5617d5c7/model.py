def reference(vectors):
    # Contract implementation.
    # State: COUNT holds current count 0..9.
    # R1_SYNC_RESET: reset==1 at posedge -> q=0 (priority 1, same cycle visible).
    # R2_COUNT_UP_WRAP: reset==0 at posedge -> q=(q+1)%10 (priority 2).
    # Mid changes occur AFTER sampling, before next edge, carried to next row.
    # Power-up unspecified: we choose q=0 as concrete value (candidate 1).
    q = 0  # R2_COUNT_UP_WRAP initial concrete value (power-up unspecified -> 0)
    out = []
    for row in vectors:
        # Sample: compute outputs based on current state and inputs at this edge.
        # R1_SYNC_RESET: reset high -> q becomes 0 (visible same cycle).
        if row.get('reset', 0) == 1:
            q = 0  # R1_SYNC_RESET
        else:
            q = (q + 1) % 10  # R2_COUNT_UP_WRAP
        out.append({'q': q})
        # Mid changes: applied after sampling, carried to next row.
        # (No mid inputs in this design beyond reset, which is a normal input.)
    return out
