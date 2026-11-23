def reference(vectors):
    cnt = 0x1F
    out = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            r = row.get('reset', 0)
        elif isinstance(row, (list, tuple)):
            r = row[-1] if len(row) else 0
        else:
            r = row
        if r:
            cnt = 0x1F
        gate = 1 if 0 < cnt < 0xE else 0
        rel = 1 if cnt < 0x8 else 0
        out.append({'cnt_q': cnt & 0x1F, 'gate_clk_o': gate, 'release_reset_o': rel})
        if (i % 2 == 0) and not r:
            if cnt > 0:
                cnt = (cnt - 1) & 0x1F
    return out
