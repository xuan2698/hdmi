def reference(vectors):
    cnt = 31
    result = []
    for i, vec in enumerate(vectors):
        if isinstance(vec, dict):
            r = vec.get('reset', 0)
            if 'clk' in vec:
                posedge = (vec['clk'] == 1)
            else:
                posedge = (i % 2 == 0)
        else:
            if isinstance(vec, (list, tuple)):
                r = vec[0] if len(vec) > 0 else 0
            else:
                r = vec
            posedge = (i % 2 == 0)

        cnt_q = cnt & 31
        gate = 1 if (cnt_q > 0 and cnt_q < 14) else 0
        release = 1 if (cnt_q < 8) else 0
        result.append({'cnt_q': cnt_q, 'gate_clk_o': gate, 'release_reset_o': release})

        if r == 1:
            cnt = 31
        elif posedge:
            if cnt > 0:
                cnt -= 1
            else:
                cnt = 0

    return result
