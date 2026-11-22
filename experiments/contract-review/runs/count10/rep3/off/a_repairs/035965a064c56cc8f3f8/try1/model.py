def reference(vectors):
    # Contract implementation for a synchronous active-high-reset decade counter.
    # State: count (0..9), initial value unspecified; we choose 0 for determinism.
    # R1: reset == 1 at posedge -> q = 0 (priority 1)
    # R2: reset == 0 && q == 9 at posedge -> q = 0 (priority 2)
    # R3: reset == 0 && q != 9 at posedge -> q = q + 1 (priority 3)
    # Mid changes occur AFTER sampling, before next edge; carried to next row.
    # Each row: values driven before sampled edge; sample after posedge settled.

    count = 0  # initial state (unspecified per spec; choose 0)
    out = []

    for row in vectors:
        # Inputs are driven before the sampled posedge.
        reset = row.get("reset", 0)

        # Sample after posedge has settled: compute next state per rules.
        # R1: active high synchronous reset
        if reset == 1:
            count = 0
        # R2: wrap from 9 to 0
        elif count == 9:
            count = 0
        # R3: increment otherwise
        else:
            count = count + 1

        # Output q reflects the state after the sampled edge (same_cycle visible).
        out.append({"q": count & 0xF})

        # Mid input changes (if any) occur AFTER sampling, before other edge,
        # and are carried to the start of the next row. Since we read inputs
        # fresh from each row dict at the start of the next iteration, any
        # "mid" changes would already be reflected in the next row's values.
        # No additional action needed here.

    return out
