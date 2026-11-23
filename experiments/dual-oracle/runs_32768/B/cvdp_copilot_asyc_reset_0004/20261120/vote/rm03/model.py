def reference(vectors):
    cnt = 0x1F
    result = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            reset = row.get('reset', 0)
        elif isinstance(row, (list, tuple)):
            reset = row[0] if len(row) > 0 else 0
        else:
            reset = row

        is_posedge = (i % 2 == 0)

        gate = 1 if (cnt > 0 and cnt < 0xE) else 0
        release = 1 if (cnt < 0x8) else 0
        result.append({
            'cnt_q': cnt,
            'gate_clk_o': gate,
            'release_reset_o': release
        })

        if reset == 1:
            cnt = 0x1F
        else:
            if is_posedge and cnt > 0:
                cnt -= 1

    return result
