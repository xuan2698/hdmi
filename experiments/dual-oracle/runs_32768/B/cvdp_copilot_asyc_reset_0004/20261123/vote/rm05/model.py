def reference(vectors):
    cnt = 0
    out = []
    for i, row in enumerate(vectors):
        reset = row.get('reset', 0)
        edge = row.get('edge', None)
        clk_val = row.get('clk', None)

        if edge is not None:
            if isinstance(edge, str):
                is_pos = edge.lower() in ('posedge', 'pos', '1', 'p')
            else:
                is_pos = bool(edge)
        elif clk_val is not None:
            is_pos = (clk_val == 1)
        else:
            is_pos = (i % 2 == 0)

        if reset == 1:
            cnt = 0x1F

        gate_en = (cnt > 0) and (cnt < 0xE)
        clk_now = 1 if (clk_val is None and is_pos) or (clk_val == 1) else 0
        gate_out = 1 if (gate_en and clk_now == 1) else 0
        release_out = 1 if (cnt < 0x8) else 0

        out.append({
            'cnt_q': cnt,
            'gate_clk_o': gate_out,
            'release_reset_o': release_out
        })

        if is_pos and reset == 0:
            if cnt > 0:
                cnt -= 1

    return out
