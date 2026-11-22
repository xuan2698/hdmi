def reference(vectors):
    # Contract implementation.
    # State: COUNT holds current count 0..9.
    # R1_SYNC_RESET: reset==1 at posedge -> q <= 0 (priority 1).
    # R2_COUNT_UP_WRAP: reset==0 at posedge -> q <= (q+1) mod 10 (priority 2).
    # Mid input changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.
    # Power-up: q is 0 (chosen interpretation).
    q = 0
    out = []
    for row in vectors:
        # Sample current outputs before the posedge (values driven before edge).
        out.append({"q": q & 0xF})
        # Apply synchronous update at posedge using this row's reset.
        reset = row.get("reset", 0) & 1
        if reset == 1:
            # R1_SYNC_RESET
            q = 0
        else:
            # R2_COUNT_UP_WRAP
            q = (q + 1) % 10
        # Mid changes (if any) are applied after sampling and carried forward;
        # they do not affect this row's output, only subsequent rows.
        # (No mid keys in this contract's vectors beyond reset, which is
        #  already consumed at the posedge.)
    return out
