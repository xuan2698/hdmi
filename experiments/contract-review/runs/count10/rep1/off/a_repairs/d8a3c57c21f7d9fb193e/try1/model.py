def reference(vectors):
    # Contract implementation for a synchronous active-high reset decade counter.
    # R1_SYNC_RESET: reset == 1 at posedge -> q = 0 (same cycle visible)
    # R2_COUNT_INC: reset == 0 at posedge -> q = (q + 1) mod 10
    # R3_WRAP: when q == 9 and reset == 0 -> q = 0
    # State: COUNT holds current decade value 0..9.
    # Power-up unspecified -> start at 0 (concrete).
    count = 0
    out = []
    for row in vectors:
        reset = row.get("reset", 0)
        # Sample at posedge: apply synchronous reset or increment.
        if reset == 1:
            # R1_SYNC_RESET
            count = 0
        else:
            # R2_COUNT_INC / R3_WRAP
            if count == 9:
                count = 0
            else:
                count = count + 1
        out.append({"q": count & 0xF})
    return out
