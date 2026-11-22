def reference(vectors):
    # Contract:
    # - 8 D flip-flops, negative-edge triggered.
    # - Active-high synchronous reset: on negedge clk, if reset==1 -> q=0x34.
    # - Otherwise on negedge clk, q = d.
    # - q holds between negedges.
    # - Power-up unspecified -> use 0x34 as concrete initial value.
    # - Each row: values driven before sampled edge; mid changes occur AFTER
    #   sampling, before the other edge, carried to start of next row.
    q = 0x34
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        reset = row.get('reset', 0)
        d = row.get('d', 0)
        # Sample at negedge clk (clk transitions 1->0). We treat clk==0 in row
        # as the sampled negedge state; apply synchronous update.
        if clk == 0:
            if reset:
                q = 0x34
            else:
                q = d & 0xFF
        out.append({'q': q & 0xFF})
    return out
