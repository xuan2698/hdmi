def reference(vectors):
    def s16(x):
        x &= 0xFFFF
        return x - 0x10000 if x >= 0x8000 else x

    out1 = out2 = out3 = 0
    results = []

    for i, row in enumerate(vectors):
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_posedge = e.lower() in ('posedge', 'pos', 'rising', '1')
            else:
                is_posedge = bool(e)
        else:
            is_posedge = (i % 2 == 0)

        rst = row.get('reset', 0)
        in1 = s16(row.get('in_1', 0))
        in2 = s16(row.get('in_2', 0))
        in3 = s16(row.get('in_3', 0))
        sel = row.get('filter_select', 0) & 3

        if rst:
            out1 = out2 = out3 = 0

        results.append({
            'out_1': out1 & 0xFFFF,
            'out_2': out2 & 0xFFFF,
            'out_3': out3 & 0xFFFF
        })

        if is_posedge and not rst:
            def update(cur, inp, s):
                nxt = cur + ((inp - cur) >> s)
                if nxt > 32767:
                    nxt = 32767
                elif nxt < -32768:
                    nxt = -32768
                return nxt

            out1 = update(out1, in1, sel)
            out2 = update(out2, in2, sel)
            out3 = update(out3, in3, sel)

    return results
