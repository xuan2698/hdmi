def reference(vectors):
    s = 0
    m = 0
    h = 0
    cnt = 0
    pulse = 0
    prev_clk = 0
    out = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = row.get('reset', 0)
            ss = row.get('start_stop', 0)
            if 'clk' in row:
                clk = row['clk']
                posedge = (clk == 1 and prev_clk == 0)
                prev_clk = clk
            else:
                posedge = (i % 2 == 0)
        else:
            rst = 0
            ss = 0
            posedge = (i % 2 == 0)
        if rst:
            s = 0
            m = 0
            h = 0
            cnt = 0
            pulse = 0
        out.append({'seconds': s, 'minutes': m, 'hour': h})
        if posedge and not rst:
            op = pulse
            oc = cnt
            os = s
            om = m
            oh = h
            if ss:
                if oc == 3:
                    nc = 0
                    np = 1
                else:
                    nc = oc + 1
                    np = 0
            else:
                nc = oc
                np = 0
            ns = os
            nm = om
            nh = oh
            if op:
                if os == 59:
                    ns = 0
                    if om == 59:
                        nm = 0
                        nh = 1
                    else:
                        nm = om + 1
                else:
                    ns = os + 1
            s = ns
            m = nm
            h = nh
            cnt = nc
            pulse = np
    return out
