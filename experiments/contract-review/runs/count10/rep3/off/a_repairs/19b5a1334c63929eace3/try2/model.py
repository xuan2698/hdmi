def reference(vectors):
    # State: count (0..9), initialized to 0 (power-up unspecified but concrete)
    count = 0
    out = []
    for row in vectors:
        # R1: reset == 1 -> synchronous reset to 0, visible same cycle (posedge)
        # R2: reset == 0 && q == 9 -> wrap to 0
        # R3: reset == 0 && q != 9 -> increment
        if row.get("reset", 0) == 1:
            count = 0  # R1
        else:
            if count == 9:
                count = 0  # R2
            else:
                count = count + 1  # R3
        out.append({"q": count & 0xF})
    return out
