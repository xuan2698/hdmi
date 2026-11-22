def reference(vectors):
    # State: Q = stored flip-flop value (unknown at power-up per candidate interpretation)
    # We model unknown initial value as 0 for concrete output, but note it's implementation-defined.
    Q = 0  # R_global: initial value unknown/implementation-defined; concrete 0 chosen

    results = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1

        # posedge clk sampling occurs here (after inputs settled)
        if r == 1:
            # R1_sync_reset: active high synchronous reset, priority 1
            Q = 0
        else:
            # R2_capture_d: capture d, priority 2
            Q = d

        # mid changes occur AFTER sampling, before other edge, carried to next row
        # (no mid changes provided in this contract's vectors; nothing to apply)

        results.append({'q': Q & 1})

    return results
