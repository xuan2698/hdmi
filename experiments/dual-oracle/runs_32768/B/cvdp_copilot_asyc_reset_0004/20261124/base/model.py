def reference(vectors):
    cnt = 0
    res = []
    for i, row in enumerate(vectors):
        reset = row.get('reset', 0)
        if reset == 1:
            cnt = 0x1F
        gate = 1 if 0 < cnt < 0xE else 0
        release = 1 if cnt < 0x8 else 0
        res.append({'cnt_q': cnt, 'gate_clk_o': gate, 'release_reset_o': release})
        if 'clk' in row:
            posedge = (row['clk'] == 1)
        else:
            posedge = (i % 2 == 0)
        if posedge:
            if reset == 1:
                cnt = 0x1F
            else:
                if cnt > 0:
                    cnt -= 1
    return res
