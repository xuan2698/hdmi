def reference(vectors):
    # State: count (0..9), initial unspecified -> use 0 for concrete outputs.
    count = 0
    out = []
    for row in vectors:
        # R1: synchronous active-high reset, priority 1, visible same cycle
        # R2: reset==0 && q==9 -> wrap to 0, priority 2
        # R3: reset==0 && q!=9 -> increment, priority 3
        if row.get("reset", 0) == 1:
            count = 0  # R1
        else:
            if count == 9:
                count = 0  # R2
            else:
                count = (count + 1) % 10  # R3
        out.append({"q": count & 0xF})
    return out
