def reference(vectors):
    q = 0
    out = []
    has_clk = any(isinstance(r, dict) and 'clk' in r for r in vectors)
    prev_clk = 0

    for row in vectors:
        if isinstance(row, dict):
            a = row.get('a', 0)
            clk = row.get('clk', None)
        else:
            if has_clk:
                clk, a = row[0], row[1]
            else:
                a = row[0]
                clk = None

        if has_clk:
            if clk is None:
                clk = 0
            if prev_clk == 0 and clk == 1:
                if a:
                    q = 4
                else:
                    q = (q + 1) % 7
            prev_clk = clk
        else:
            if a:
                q = 4
            else:
                q = (q + 1) % 7

        out.append({'q': q})

    return out
