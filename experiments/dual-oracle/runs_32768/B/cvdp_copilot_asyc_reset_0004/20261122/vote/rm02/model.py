def reference(vectors):
    cnt = 0
    out = []
    if vectors and vectors[0].get('reset', 0) == 1:
        cnt = 31
    for i, row in enumerate(vectors):
        reset = row.get('reset', 0)
        c = cnt & 31
        out.append({
            'cnt_q': c,
            'gate_clk_o': 1 if 0 < c < 14 else 0,
            'release_reset_o': 1 if c < 8 else 0
        })
        if reset:
            cnt = 31
        elif i % 2 == 0:
            if cnt > 0:
                cnt -= 1
    return out
