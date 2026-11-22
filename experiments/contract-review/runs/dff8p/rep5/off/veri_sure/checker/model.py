def reference(vectors):
    # Contract:
    # - 8 D flip-flops, negative-edge triggered on clk.
    # - Active-high synchronous reset: at negedge, if reset==1 -> q = 0x34.
    # - Otherwise at negedge, q = d.
    # - q holds between negedges.
    # - Power-up state is unspecified; we use 0x34 as a concrete initial value.
    # - Each row: inputs are driven before the sampled negedge.
    # - Mid input changes occur AFTER sampling, before the other edge,
    #   and carry to the start of the next row.
    q = 0x34
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        reset = row.get('reset', 0)
        d = row.get('d', 0)
        # Sample at negedge: clk transitions 1->0
        # We treat the row's clk as the value at the sampled edge.
        # A negedge is when clk == 0 (the settled value after the edge).
        if clk == 0:
            if reset:
                q = 0x34
            else:
                q = d & 0xFF
        out.append({'q': q & 0xFF})
    return out
