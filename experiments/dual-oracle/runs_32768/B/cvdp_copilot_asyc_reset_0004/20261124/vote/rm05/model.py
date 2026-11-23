def reference(vectors):
    cnt = 0
    result = []
    for v in vectors:
        if isinstance(v, dict):
            reset = int(v.get('reset', 0)) & 1
            edge = v.get('edge', 0)
        else:
            reset = 0
            edge = 0
            if isinstance(v, (list, tuple)):
                for x in v:
                    if isinstance(x, str):
                        edge = x
                    elif isinstance(x, (int, bool)):
                        reset = int(x) & 1
            else:
                reset = int(v) & 1
        if isinstance(edge, str):
            e = edge.lower()
            posedge = ('pos' in e) or ('ris' in e)
        else:
            posedge = bool(edge)
        if reset:
            cnt = 31
        en = 1 if (cnt > 0 and cnt < 14) else 0
        clk_val = 1 if posedge else 0
        gate = en & clk_val
        rel = 1 if cnt < 8 else 0
        result.append({'cnt_q': cnt, 'gate_clk_o': gate, 'release_reset_o': rel})
        if posedge and not reset and cnt > 0:
            cnt -= 1
    return result
