def reference(vectors):
    cnt = 0x1F
    out = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            edge = row.get('edge', 'posedge' if i % 2 == 0 else 'negedge')
        elif isinstance(row, (list, tuple)):
            reset = 0
            edge = None
            for v in row:
                if isinstance(v, str):
                    edge = v
                else:
                    reset = v
            if edge is None:
                edge = 'posedge' if i % 2 == 0 else 'negedge'
        else:
            reset = row
            edge = 'posedge' if i % 2 == 0 else 'negedge'

        if reset:
            cnt = 0x1F

        gate = 1 if 0 < cnt < 0xE else 0
        rel = 1 if cnt < 0x8 else 0
        out.append({'cnt_q': cnt & 0x1F, 'gate_clk_o': gate, 'release_reset_o': rel})

        if isinstance(edge, str) and edge.lower().startswith('pos') and not reset:
            if cnt > 0:
                cnt = (cnt - 1) & 0x1F

    return out
