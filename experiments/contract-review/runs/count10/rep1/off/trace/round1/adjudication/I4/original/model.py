def reference(vectors):
    # Contract implementation.
    # State: COUNT (current decade count 0..9), updated on posedge.
    # Output q reflects COUNT after the sampled posedge.
    # R1_SYNC_RESET: reset==1 on posedge -> q=0 (priority 0).
    # R2_COUNT_INC: reset==0 -> q = (q+1) mod 10.
    # R3_WRAP: q==9 and reset==0 -> q=0.
    # Mid changes occur AFTER sampling, carried to next row.

    count = 0  # power-up unspecified; use 0 as concrete value
    results = []

    for row in vectors:
        reset = row.get("reset", 0)
        # Sample at posedge: apply synchronous reset / count logic.
        if reset == 1:
            # R1_SYNC_RESET
            count = 0
        else:
            # R2_COUNT_INC / R3_WRAP
            if count == 9:
                count = 0  # R3_WRAP
            else:
                count = count + 1  # R2_COUNT_INC
        # Output visible same cycle
        results.append({"q": count & 0xF})

    return results
