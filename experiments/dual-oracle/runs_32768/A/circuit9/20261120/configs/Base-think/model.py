def reference(vectors):
    q = 0
    current_a = 0
    prev_clk = 0
    res = []
    for row in vectors:
        clk = row.get('clk', prev_clk)
        a = row.get('a', current_a)
        if prev_clk == 0 and clk == 1:
            if a == 1:
                q = 4
            else:
                q = (q + 1) % 7
        res.append({'q': q})
        current_a = a
        if 'mid' in row:
            mid = row['mid']
            if 'a' in mid:
                current_a = mid['a']
        prev_clk = clk
    return res
