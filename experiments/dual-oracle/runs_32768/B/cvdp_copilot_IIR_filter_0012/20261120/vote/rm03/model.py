def reference(vectors):
    y1 = y2 = y3 = 0
    prev_clk = 0
    res = []
    for row in vectors:
        if isinstance(row, dict):
            clk = row.get('clk', None)
            rst = int(row.get('reset', 0))
            in1 = row.get('in_1', 0)
            in2 = row.get('in_2', 0)
            in3 = row.get('in_3', 0)
            sel = int(row.get('filter_select', 0)) & 3
            edge = row.get('edge', None)
        else:
            clk = row[0] if len(row) > 0 else None
            rst = int(row[1]) if len(row) > 1 else 0
            in1 = row[2] if len(row) > 2 else 0
            in2 = row[3] if len(row) > 3 else 0
            in3 = row[4] if len(row) > 4 else 0
            sel = int(row[5]) & 3 if len(row) > 5 else 0
            edge = None

        def s16(v):
            v = int(v) & 0xFFFF
            return v - 0x10000 if v >= 0x8000 else v

        in1 = s16(in1)
        in2 = s16(in2)
        in3 = s16(in3)

        is_pos = False
        if edge is not None:
            if isinstance(edge, str):
                is_pos = 'pos' in edge.lower()
            else:
                is_pos = (int(edge) == 1)
        elif clk is not None:
            c = int(clk) & 1
            if c == 1 and prev_clk == 0:
                is_pos = True

        if rst:
            y1 = y2 = y3 = 0

        res.append({
            'out_1': y1 & 0xFFFF,
            'out_2': y2 & 0xFFFF,
            'out_3': y3 & 0xFFFF
        })

        if is_pos and not rst:
            gain = sel + 1

            def sat16(v):
                if v > 32767:
                    return 32767
                if v < -32768:
                    return -32768
                return v

            y1 = sat16(in1 * gain)
            y2 = sat16(in2 * gain)
            y3 = sat16(in3 * gain)

        if clk is not None:
            prev_clk = int(clk) & 1

    return res
