def reference(vectors):
    def s16(v):
        v = int(v) & 0xFFFF
        return v - 0x10000 if v & 0x8000 else v

    def clamp(v):
        if v > 32767:
            return 32767
        if v < -32768:
            return -32768
        return v

    out1 = out2 = out3 = 0
    prev1 = prev2 = prev3 = 0
    res = []

    for i, row in enumerate(vectors):
        reset = int(row.get('reset', 0)) & 1

        if reset:
            out1 = out2 = out3 = 0
            prev1 = prev2 = prev3 = 0
            res.append({'out_1': 0, 'out_2': 0, 'out_3': 0})
            continue

        if 'edge' in row:
            is_pos = str(row['edge']).lower() in ('posedge', 'pos', '1')
        else:
            is_pos = (i % 2 == 0)

        res.append({
            'out_1': out1 & 0xFFFF,
            'out_2': out2 & 0xFFFF,
            'out_3': out3 & 0xFFFF
        })

        if is_pos:
            x1 = s16(row.get('in_1', 0))
            x2 = s16(row.get('in_2', 0))
            x3 = s16(row.get('in_3', 0))
            fs = int(row.get('filter_select', 0)) & 3

            def apply_filter(x, p):
                if fs == 0:
                    y = x
                elif fs == 1:
                    y = (x + p) >> 1
                elif fs == 2:
                    y = x - p
                else:
                    y = x + p
                return clamp(y)

            out1 = apply_filter(x1, prev1)
            out2 = apply_filter(x2, prev2)
            out3 = apply_filter(x3, prev3)

            prev1, prev2, prev3 = x1, x2, x3

    return res
