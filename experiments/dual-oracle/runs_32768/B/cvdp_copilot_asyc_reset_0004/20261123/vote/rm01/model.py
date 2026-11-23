def reference(vectors):
    cnt = 0x1F
    out = []
    for i, row in enumerate(vectors):
        reset = 0
        edge = None
        clk = None
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            edge = row.get('edge', None)
            clk = row.get('clk', None)
        elif isinstance(row, (list, tuple)):
            if len(row) == 1:
                reset = row[0]
            elif len(row) >= 2:
                if isinstance(row[0], str) and ('pos' in row[0].lower() or 'neg' in row[0].lower()):
                    edge = row[0]
                    reset = row[1]
                else:
                    clk = row[0]
                    reset = row[1]
        else:
            reset = row
        
        rst = 1 if (reset is True or reset == 1 or reset == '1') else 0
        
        pos = False
        if edge is not None:
            if isinstance(edge, str):
                e = edge.lower()
                if 'pos' in e:
                    pos = True
                elif 'neg' in e:
                    pos = False
                else:
                    pos = (edge == '1')
            else:
                pos = (edge == 1 or edge is True)
        elif clk is not None:
            pos = (clk is True or clk == 1 or clk == '1')
        else:
            pos = (i % 2 == 0)
        
        if rst:
            cnt = 0x1F
        
        gate = 1 if (cnt > 0 and cnt < 0xE) else 0
        release = 1 if cnt < 0x8 else 0
        out.append({'cnt_q': cnt & 0x1F, 'gate_clk_o': gate, 'release_reset_o': release})
        
        if pos:
            if rst:
                cnt = 0x1F
            else:
                if cnt > 0:
                    cnt = (cnt - 1) & 0x1F
    return out
