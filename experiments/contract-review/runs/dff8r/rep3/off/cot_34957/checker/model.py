def reference(vectors):
    # 8 D flip-flops, active-high synchronous reset, positive-edge clk.
    # q_next = 0x00 if reset else d, sampled at posedge.
    # Power-up unspecified: first sampled edge establishes q.
    q = None
    out = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1
        # At the sampled posedge, compute next state from current inputs.
        if reset:
            q = 0x00
        else:
            q = d
        out.append({'q': q & 0xFF})
    return out
