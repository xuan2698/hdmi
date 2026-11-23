def reference(vectors):
    q = 0
    prev_clk = 0
    out = []
    for row in vectors:
        if isinstance(row, dict):
            d = row.get('d', 0)
            reset = row.get('reset', 0)
            clk = row.get('clk', None)
        else:
            d = row[0] if len(row) > 0 else 0
            reset = row[1] if len(row) > 1 else 0
            clk = row[2] if len(row) > 2 else None
        if clk is None:
            edge = True
        else:
            edge = (prev_clk == 0 and clk == 1)
            prev_clk = clk
        if edge:
            if reset:
                q = 0
            else:
                q = d & 255
        out.append({'q': q})
    return out
