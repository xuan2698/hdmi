def reference(vectors):
    q = 0
    prev_a = 0
    outputs = []
    for row in vectors:
        clk = row.get('clk', 1)
        a = row.get('a', 0)
        if clk == 1:
            # R1_a_high_load4
            if a == 1:
                q = 4
            else:
                # R2_first_low_hold
                if prev_a == 1:
                    q = q
                else:
                    # R3_count_low
                    q = (q + 1) % 7
            prev_a = a
        outputs.append({'q': q})
    return outputs
