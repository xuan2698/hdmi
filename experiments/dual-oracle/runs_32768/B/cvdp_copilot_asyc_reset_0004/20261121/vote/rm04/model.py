def reference(vectors):
    cnt = 0x1F
    out = []
    for i, row in enumerate(vectors):
        reset = row.get('reset', 0) if isinstance(row, dict) else row
        if reset:
            cnt = 0x1F
        gate = 1 if (cnt > 0 and cnt < 0xE) else 0
        release = 1 if (cnt < 0x8) else 0
        out.append({'cnt_q': cnt & 0x1F, 'gate_clk_o': gate, 'release_reset_o': release})
        if i % 2 == 0:
            if not reset:
                if cnt > 0:
                    cnt = (cnt - 1) & 0x1F
                else:
                    cnt = 0
    return out
