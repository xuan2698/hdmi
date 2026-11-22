def reference(vectors):
    # Contract:
    # - 8 D flip-flops, negative-edge triggered on clk.
    # - Active-high synchronous reset: on negedge clk, if reset==1 -> q=0x34.
    # - Otherwise on negedge clk, q = d.
    # - q holds between negedges.
    # - Power-up state: unspecified; we model as 0x34 (reset value) for concreteness.
    # - Each row: inputs driven before sampled edge; mid changes occur AFTER sampling,
    #   before the other edge, carried to start of next row.
    q = 0x34  # power-up model (unspecified; use reset value)
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        reset = row.get('reset', 0)
        d = row.get('d', 0)
        # Sample on negedge: detect clk transition 1->0
        prev_clk = row.get('_prev_clk', None)
        # We track prev clk across rows via a mutable marker
        # Since we can't store state outside, use a sentinel in the dict? No—use closure var.
        # We'll track prev_clk in a local variable updated each iteration.
        # But mid changes: the row's clk value is the value at sampling time.
        # We assume each row represents the state at the sampled negedge.
        # So we just apply the flip-flop update if this row is a negedge sample.
        # The protocol says "sample after the negedge edge has settled" — so each row
        # corresponds to a negedge event. We apply update each row.
        if reset:
            q = 0x34
        else:
            q = d & 0xFF
        out.append({'q': q & 0xFF})
    return out
