def reference(vectors):
    # State: COUNT holds current count 0..9
    # R1_SYNC_RESET: reset==1 at posedge -> q=0 (priority 1)
    # R2_COUNT_UP_WRAP: reset==0 at posedge -> q=(q+1)%10 (priority 2)
    # Power-up unspecified: initialize to 0 (concrete value required)
    count = 0
    out = []
    for row in vectors:
        # Sample inputs driven before the posedge
        reset = row.get('reset', 0)
        # Apply posedge transition
        if reset == 1:  # R1_SYNC_RESET
            count = 0
        else:  # R2_COUNT_UP_WRAP
            count = (count + 1) % 10
        # Output visible same cycle
        out.append({'q': count & 0xF})
        # Mid changes occur AFTER sampling, before other edge; carried to next row
        # (no state change needed here since next row reads its own inputs)
    return out
