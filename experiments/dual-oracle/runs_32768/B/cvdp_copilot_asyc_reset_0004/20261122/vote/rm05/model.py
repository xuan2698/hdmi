def reference(vectors):
    cnt = 0x1F
    out = []
    for i, row in enumerate(vectors):
        rst = int(row.get('reset', 0))
        gate = 1 if (0 < cnt < 0xE) else 0
        rel = 1 if (cnt < 0x8) else 0
        out.append({'cnt_q': cnt, 'gate_clk_o': gate, 'release_reset_o': rel})
        posedge = (int(row['clk']) == 1) if 'clk' in row else (i % 2 == 0)
        if rst == 1:
            cnt = 0x1F
        elif posedge:
            if cnt > 0:
                cnt -= 1
    return out
