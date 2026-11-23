def reference(vectors):
    out1 = out2 = out3 = 0
    result = []
    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            r = int(row.get('reset', 0)) & 1
            i1 = row.get('in_1', 0)
            i2 = row.get('in_2', 0)
            i3 = row.get('in_3', 0)
            edge = row.get('edge', None)
            clk = row.get('clk', None)
        else:
            try:
                r = int(row.reset) & 1
                i1 = row.in_1
                i2 = row.in_2
                i3 = row.in_3
                edge = getattr(row, 'edge', None)
                clk = getattr(row, 'clk', None)
            except Exception:
                r = i1 = i2 = i3 = edge = clk = 0

        if r:
            out1 = out2 = out3 = 0

        result.append({
            'out_1': out1 & 0xFFFF,
            'out_2': out2 & 0xFFFF,
            'out_3': out3 & 0xFFFF
        })

        pos = False
        if edge is not None:
            if isinstance(edge, str):
                e = edge.lower()
                if 'pos' in e or e == '1':
                    pos = True
                elif 'neg' in e or e == '0':
                    pos = False
                else:
                    pos = (idx % 2 == 0)
            else:
                pos = bool(edge)
        elif clk is not None:
            pos = (int(clk) & 1) == 1
        else:
            pos = (idx % 2 == 0)

        if pos:
            if r:
                out1 = out2 = out3 = 0
            else:
                out1 = int(i1) & 0xFFFF
                out2 = int(i2) & 0xFFFF
                out3 = int(i3) & 0xFFFF

    return result
