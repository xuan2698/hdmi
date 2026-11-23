def reference(vectors):
    cnt = 0x1F
    out = []
    for i, row in enumerate(vectors):
        reset = 0
        clk_level = 1 if (i % 2 == 0) else 0
        posedge = (i % 2 == 0)
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            if 'clk' in row:
                clk_level = row['clk']
                posedge = (clk_level == 1)
            elif 'edge' in row:
                e = row['edge']
                if e == 1 or e == 'posedge' or e == 'pos' or e is True:
                    clk_level = 1
                    posedge = True
                elif e == 0 or e == 'negedge' or e == 'neg' or e is False:
                    clk_level = 0
                    posedge = False
            elif 'posedge' in row:
                posedge = bool(row['posedge'])
                clk_level = 1 if posedge else 0
        else:
            if isinstance(row, (list, tuple)):
                if len(row) > 0:
                    reset = row[0]
                if len(row) > 1:
                    clk_level = row[1]
                    posedge = (clk_level == 1)
            else:
                reset = row
        reset = 1 if reset else 0
        gate_cond = 1 if (cnt > 0 and cnt < 0xE) else 0
        gate_clk = gate_cond & (1 if clk_level else 0)
        release = 1 if (cnt < 0x8) else 0
        out.append({
            'cnt_q': cnt & 0x1F,
            'gate_clk_o': gate_clk & 1,
            'release_reset_o': release & 1
        })
        if reset:
            cnt = 0x1F
        elif posedge:
            if cnt > 0:
                cnt -= 1
    return out
