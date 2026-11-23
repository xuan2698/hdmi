def reference(vectors):
    cnt = 0
    out = []
    prev_clk = 0
    for idx, row in enumerate(vectors):
        reset = 0
        edge = None
        clk_val = None
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    s = e.lower()
                    if 'pos' in s:
                        edge = 'posedge'
                    elif 'neg' in s:
                        edge = 'negedge'
                    else:
                        edge = 'posedge' if idx % 2 == 0 else 'negedge'
                else:
                    edge = 'posedge' if e else 'negedge'
                clk_val = 1 if edge == 'posedge' else 0
            elif 'clk' in row:
                clk_val = row['clk'] & 1
                if clk_val == 1 and prev_clk == 0:
                    edge = 'posedge'
                elif clk_val == 0 and prev_clk == 1:
                    edge = 'negedge'
                else:
                    edge = 'posedge' if clk_val == 1 else 'negedge'
                prev_clk = clk_val
        if edge is None:
            edge = 'posedge' if idx % 2 == 0 else 'negedge'
            clk_val = 1 if edge == 'posedge' else 0
        if reset == 1:
            cnt = 31
        gate_en = 1 if (cnt > 0 and cnt < 14) else 0
        gate_clk_o = gate_en & (clk_val if clk_val is not None else 0)
        release_reset_o = 1 if cnt < 8 else 0
        out.append({
            'cnt_q': cnt,
            'gate_clk_o': gate_clk_o,
            'release_reset_o': release_reset_o
        })
        if edge == 'posedge' and reset == 0 and cnt > 0:
            cnt -= 1
    return out
