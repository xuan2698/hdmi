def reference(vectors):
    # State: count (0..9), initialized to 0 at power-up (unspecified but we pick 0)
    count = 0
    out = []
    for row in vectors:
        # Sample inputs at posedge (values driven before sampled edge)
        reset = row.get('reset', 0)
        # R1: reset == 1 -> q = 0 (priority 1)
        if reset == 1:
            count = 0
        # R2: reset == 0 && q == 9 -> wrap to 0 (priority 2)
        elif count == 9:
            count = 0
        # R3: reset == 0 && q != 9 -> increment (priority 3)
        else:
            count = count + 1
        # Output visible same cycle
        out.append({'q': count & 0xF})
    return out
