def reference(vectors):
    # State: Q is the 8-bit flip-flop output register, reset value 0x34.
    # Initial value before first negedge is unspecified; we use 0x34 (candidate).
    Q = 0x34  # R1: reset value 0x34

    results = []
    for vec in vectors:
        d = vec["d"] & 0xFF
        reset = vec["reset"] & 0x1

        # negedge sampling: apply synchronous reset or load d
        if reset == 1:
            # R1: active high synchronous reset, priority 1, visible same cycle
            Q = 0x34
        else:
            # R2: reset == 0, load d on negedge, visible same cycle
            Q = d

        results.append({"q": Q & 0xFF})

    return results
