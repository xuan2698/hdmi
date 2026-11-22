def reference(vectors):
    # 8 D flip-flops, active-high synchronous reset to 0x34, negative-edge triggered.
    # State persists across rows. Power-up q is unspecified; we model it as 0x34
    # (any value is acceptable before the first sampled edge, but we must return
    # a concrete unsigned int within 8 bits for every row).
    q = 0x34
    out = []
    for row in vectors:
        # Pre-edge inputs for this row (values driven before the sampled negedge).
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1
        # At the settled negative edge: synchronous reset takes priority.
        if reset:
            q = 0x34
        else:
            q = d
        out.append({'q': q & 0xFF})
    return out
