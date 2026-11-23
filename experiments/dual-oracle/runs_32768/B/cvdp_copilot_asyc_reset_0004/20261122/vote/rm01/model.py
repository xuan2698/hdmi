def reference(vectors):
    cnt = 31
    out = []
    i = 0
    for row in vectors:
        if isinstance(row, dict):
            rv = row.get('reset', 0)
        elif isinstance(row, (list, tuple)):
            rv = row[0] if len(row) > 0 else 0
        else:
            rv = row

        r = int(rv) & 1
        if r:
            cnt = 31

        posedge = (i % 2 == 0)
        clk = 1 if posedge else 0

        gate = clk if (cnt > 0 and cnt < 14) else 0
        release = 1 if cnt < 8 else 0

        out.append({
            'cnt_q': cnt & 31,
            'gate_clk_o': gate & 1,
            'release_reset_o': release & 1
        })

        if posedge and r == 0 and cnt > 0:
            cnt -= 1

        i += 1

    return out
