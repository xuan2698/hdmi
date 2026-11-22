def reference(vectors):
    # 8 D flip-flops, active-high synchronous reset, posedge clk.
    # State is unspecified at power-up; first sampled edge establishes it.
    q = None
    out = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1
        # At the sampled posedge, capture d and reset.
        if reset:
            q = 0
        else:
            q = d
        out.append({'q': q & 0xFF})
    return out
