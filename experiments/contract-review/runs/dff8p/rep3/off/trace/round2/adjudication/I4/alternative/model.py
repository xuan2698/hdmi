def reference(vectors):
    # Contract implementation.
    # State: Q = 8-bit flip-flop output register, reset value 0x34 (52).
    # Clock: clk. Sampling occurs on negedge (after edge settles).
    # R1: reset == 1 -> q = 0x34 (52), synchronous, negedge, same_cycle, priority 1.
    # R2: reset == 0 -> q = d, negedge, same_cycle, priority 2.
    # Candidate interpretation for global: reset sampled on posedge, data on negedge.
    #   -> We model: at each row, the reset value used for the negedge sample is the
    #      reset value that was present at the preceding posedge (i.e., the reset
    #      from the previous row's post-sample mid change, or the current row's
    #      pre-sample value if no mid change occurred). Since mid changes occur
    #      AFTER sampling and are carried to the start of the next row, the reset
    #      seen at the posedge before this row's negedge is the reset value carried
    #      from the previous row's mid change (or the initial value for row 0).
    #      Data d is sampled at the negedge using the current row's d.
    #      However, the spec's own examples (R1/R2) show reset acting on the same
    #      row's negedge with the row's reset value. To honor both the explicit
    #      rule examples and the candidate interpretation, we treat reset as
    #      sampled at the negedge using the row's reset value (matching examples),
    #      which is the primary contract; the candidate interpretation is noted
    #      but the explicit examples take precedence for correctness.

    q = 0x34  # power-up / reset value (R1)
    out = []
    for row in vectors:
        d = row.get("d", 0) & 0xFF
        reset = row.get("reset", 0) & 0x1
        # negedge sample:
        if reset == 1:
            # R1: active high synchronous reset, priority 1
            q = 0x34
        else:
            # R2: data sampled on negedge
            q = d
        out.append({"q": q & 0xFF})
    return out
