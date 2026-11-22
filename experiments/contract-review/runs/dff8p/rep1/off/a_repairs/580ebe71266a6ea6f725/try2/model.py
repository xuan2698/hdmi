def reference(vectors):
    # State: q_state holds the 8-bit value stored in the D flip-flops.
    # Initial value is unspecified at power-up; we start at 0x34 (reset value)
    # since the contract's reset value is 0x34 and first sampled edge applies it.
    q_state = 0x34  # R1: reset value 0x34

    outputs = []
    for row in vectors:
        d = row["d"]
        reset = row["reset"]

        # R1: active high synchronous reset, priority 1, negedge, same_cycle
        # R2: reset == 0, negedge, same_cycle -> q <= d
        if reset == 1:
            q_state = 0x34  # R1
        else:
            q_state = d & 0xFF  # R2

        outputs.append({"q": q_state & 0xFF})

    return outputs
