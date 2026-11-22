def reference(vectors):
    # Contract implementation for a synchronous active-high reset decade counter.
    # State: COUNT (0..9). Output q reflects COUNT after the sampled posedge.
    # R1_SYNC_RESET: reset==1 at posedge -> q=0 (same cycle visible)
    # R2_COUNT_INC: reset==0 at posedge -> q = (q+1) mod 10
    # R3_WRAP: when q==9 and reset==0 -> q=0
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.

    q = 0  # power-up unspecified; start at 0
    out = []

    for row in vectors:
        reset = row.get("reset", 0)
        # Sample at posedge: apply synchronous reset or increment
        if reset == 1:
            # R1_SYNC_RESET
            q = 0
        else:
            # R2_COUNT_INC / R3_WRAP
            q = (q + 1) % 10
        out.append({"q": q & 0xF})

        # Mid changes: applied after sampling, carried to next row.
        # (No mid inputs defined in this contract beyond reset, which is
        #  already the row's driven value; nothing extra to apply.)

    return out
