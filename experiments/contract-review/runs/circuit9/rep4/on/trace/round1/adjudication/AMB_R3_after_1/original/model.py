def reference(vectors):
    # Concrete initial values for unspecified power-up
    q = 0
    prev_a = 0
    prev_clk = 0
    results = []

    # Detect whether clock is explicitly provided in the vectors
    has_clk = False
    for v in vectors:
        if 'clk' in v:
            has_clk = True
            break

    for vec in vectors:
        a = vec.get('a', 0)

        if has_clk:
            clk = vec.get('clk', 0)
            posedge = (clk == 1 and prev_clk == 0)
            prev_clk = clk
        else:
            # Each row represents one sampled posedge when clock is implicit
            posedge = True

        if posedge:
            # R1_a_high_load4: a == 1 at posedge => q <= 4
            if a == 1:
                q = 4
            # R2_first_low_hold: a == 0 && prev_a == 1 at posedge => q holds
            elif prev_a == 1:
                q = q
            # R3_count_low: a == 0 && prev_a == 0 at posedge => q <= (q + 1) mod 7
            else:
                q = (q + 1) % 7
            prev_a = a

        results.append({'q': q})

    return results
