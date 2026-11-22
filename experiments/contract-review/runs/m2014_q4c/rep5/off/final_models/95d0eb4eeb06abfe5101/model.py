def reference(vectors):
    # Contract implementation for a 1-bit D flip-flop with active-high
    # synchronous reset.
    #
    # State:
    #   Q : stored flip-flop value (unspecified before first posedge with r==0)
    #
    # Timing:
    #   - Each row's inputs are driven before the sampled posedge.
    #   - Sampling happens at posedge clk (after settling).
    #   - Optional mid input changes occur AFTER sampling, before the other
    #     edge, and are carried to the start of the next row.
    #
    # Rules:
    #   R1: r == 1 at posedge -> q = 0 (synchronous reset, priority 1)
    #   R2: r == 0 at posedge -> q = d (D flip-flop load, priority 2)

    Q = None  # unspecified before first posedge with r == 0
    out = []

    for row in vectors:
        d = int(row["d"]) & 1
        r = int(row["r"]) & 1

        # R1: active high synchronous reset (priority 1)
        if r == 1:
            Q = 0
        # R2: D flip-flop load when not reset (priority 2)
        else:
            Q = d

        # Output visible same cycle as the sampled posedge.
        # If Q is still unspecified (no posedge with r==0 yet), we must
        # still return a concrete unsigned integer within 1 bit.
        q_val = 0 if Q is None else (Q & 1)
        out.append({"q": q_val})

    return out
