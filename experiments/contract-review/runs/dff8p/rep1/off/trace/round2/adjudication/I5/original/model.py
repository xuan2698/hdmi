def reference(vectors):
    # State: q_state holds the 8-bit value stored in the D flip-flops.
    # Updated on the negative edge of clk.
    q_state = 0x34  # power-up unspecified; use reset value as concrete default

    out = []
    for row in vectors:
        d = row["d"] & 0xFF
        reset = row["reset"] & 0x1

        # R1: active high synchronous reset -> q = 0x34 on negedge (priority 1)
        # R2: otherwise q = d on negedge (priority 2)
        if reset == 1:
            q_state = 0x34  # R1
        else:
            q_state = d  # R2

        out.append({"q": q_state & 0xFF})

    return out
