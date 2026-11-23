def reference(vectors):
    cnt = 0
    res = []
    for i, v in enumerate(vectors):
        if isinstance(v, dict):
            reset = v.get('reset', 0)
        elif isinstance(v, (list, tuple)):
            reset = v[0] if len(v) > 0 else 0
        else:
            reset = v

        if reset == 1:
            cnt = 31

        clk_val = 1 if (i % 2 == 0) else 0
        enable = 1 if (cnt > 0 and cnt < 14) else 0
        gate = enable if clk_val == 1 else 0
        release = 1 if cnt < 8 else 0

        res.append({
            'cnt_q': cnt,
            'gate_clk_o': gate,
            'release_reset_o': release
        })

        if i % 2 == 0 and reset == 0:
            if cnt > 0:
                cnt -= 1

    return res
