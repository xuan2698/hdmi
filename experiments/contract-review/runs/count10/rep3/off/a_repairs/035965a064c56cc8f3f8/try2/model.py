def reference(vectors):
    # Contract implementation.
    # State: count (0..9), initial value unspecified -> choose 0 for determinism.
    # R1: reset == 1 at posedge -> q = 0 (sync, active high, priority 1)
    # R2: reset == 0 && q == 9 at posedge -> q = 0 (priority 2)
    # R3: reset == 0 && q != 9 at posedge -> q = q + 1 (priority 3)
    # Mid changes occur AFTER sampling, before next edge; carried to next row.
    # Each row: values driven before sampled edge; sample after posedge settled.
    count = 0
    out = []
    for row in vectors:
        # Sample at posedge with current inputs (mid changes from prior row already applied)
        reset = row.get('reset', 0)
        # R1
        if reset == 1:
            count = 0
        # R2
        elif count == 9:
            count = 0
        # R3
        else:
            count = count + 1
        out.append({'q': count & 0xF})
        # Apply mid changes after sampling (carried to next row start)
        # Mid changes are already reflected in next row's inputs, so nothing extra needed here.
    return out
