def reference(vectors):
    # Contract:
    # - 8 D flip-flops, negedge clk triggered.
    # - Active-high synchronous reset loads 0x34 at negedge.
    # - Otherwise q <= d at negedge.
    # - q holds between negedges.
    # - Power-up unspecified: use 0x34 as concrete initial value.
    q = 0x34
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        reset = row.get('reset', 0)
        d = row.get('d', 0)
        # Sample at negedge: row values are driven before the sampled edge.
        if clk == 0:
            if reset:
                q = 0x34
            else:
                q = d & 0xFF
        out.append({'q': q & 0xFF})
    return out
