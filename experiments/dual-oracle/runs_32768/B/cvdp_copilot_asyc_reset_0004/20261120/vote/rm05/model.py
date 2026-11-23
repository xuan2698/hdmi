def reference(vectors):
    q = 0x1F
    result = []
    for i, v in enumerate(vectors):
        if isinstance(v, dict):
            reset = int(v.get('reset', 0)) & 1
        else:
            reset = int(v) & 1 if isinstance(v, int) else 0

        if reset:
            q = 0x1F

        cnt = q & 0x1F
        gate = 1 if (cnt > 0 and cnt < 0xE) else 0
        release = 1 if cnt < 0x8 else 0

        result.append({
            'cnt_q': cnt,
            'gate_clk_o': gate,
            'release_reset_o': release
        })

        if i % 2 == 0:
            if reset:
                q = 0x1F
            else:
                if q > 0:
                    q = (q - 1) & 0x1F
                else:
                    q = 0

    return result
