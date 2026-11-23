def reference(vectors):
    o1 = o2 = o3 = 0
    ans = []
    prev_clk = None
    for i, row in enumerate(vectors):
        reset = row.get('reset', 0)
        if reset:
            o1 = o2 = o3 = 0

        edge = row.get('edge', None)
        clk = row.get('clk', None)

        if edge is not None:
            e = str(edge).lower()
            if e in ('posedge', 'pos', 'positive', 'rise', 'rising', '1', 'true'):
                pos = True
            elif e in ('negedge', 'neg', 'negative', 'fall', 'falling', '0', 'false'):
                pos = False
            else:
                pos = bool(edge)
        elif clk is not None:
            c = int(clk)
            if prev_clk is None:
                pos = (c == 1)
            else:
                pos = (prev_clk == 0 and c == 1)
            prev_clk = c
        else:
            pos = (i % 2 == 0)

        ans.append({
            'out_1': int(o1) & 0xFFFF,
            'out_2': int(o2) & 0xFFFF,
            'out_3': int(o3) & 0xFFFF
        })

        if pos and not reset:
            o1 = int(row.get('in_1', 0)) & 0xFFFF
            o2 = int(row.get('in_2', 0)) & 0xFFFF
            o3 = int(row.get('in_3', 0)) & 0xFFFF

    return ans
