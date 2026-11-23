def reference(vectors):
    state = 0
    prev_a = 0
    prev_b = 0
    prev_clk = 0
    has_clk = False
    if vectors:
        first = vectors[0]
        if isinstance(first, dict) and 'clk' in first:
            has_clk = True
    out = []
    for row in vectors:
        if isinstance(row, dict):
            a = row.get('a', 0)
            b = row.get('b', 0)
        else:
            a = row[0] if len(row) > 0 else 0
            b = row[1] if len(row) > 1 else 0
        if a == 'x' or a is None:
            a = 0
        if b == 'x' or b is None:
            b = 0
        a = int(a) & 1
        b = int(b) & 1
        if has_clk:
            clk = row.get('clk', 0) if isinstance(row, dict) else (row[2] if len(row) > 2 else 0)
            if clk == 'x' or clk is None:
                clk = 0
            clk = int(clk) & 1
            if prev_clk == 0 and clk == 1:
                s = state + prev_a + prev_b
                state = 1 if s >= 2 else 0
            prev_clk = clk
        else:
            s = state + prev_a + prev_b
            state = 1 if s >= 2 else 0
        q = (a ^ b ^ state) & 1
        out.append({'q': q, 'state': state})
        prev_a = a
        prev_b = b
    return out
