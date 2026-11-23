def reference(vectors):
    st = 31
    out = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = row.get('reset', 0)
        elif isinstance(row, (list, tuple)):
            rst = row[0] if len(row) > 0 else 0
        else:
            rst = row
        if rst:
            st = 31
        gate = 1 if (st > 0 and st < 14) else 0
        rel = 1 if st < 8 else 0
        out.append({'cnt_q': st, 'gate_clk_o': gate, 'release_reset_o': rel})
        if i % 2 == 0 and not rst and st > 0:
            st -= 1
    return out
