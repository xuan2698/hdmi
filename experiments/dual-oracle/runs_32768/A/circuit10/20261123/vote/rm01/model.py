def reference(vectors):
    state = 0
    prev_clk = 0
    last_a = 0
    last_b = 0
    result = []
    for row in vectors:
        if isinstance(row, dict):
            clk = row.get('clk', 0)
            a = row.get('a', 0)
            b = row.get('b', 0)
        else:
            if len(row) >= 3:
                clk, a, b = row[0], row[1], row[2]
            else:
                clk = 0
                a, b = row[0], row[1]

        if clk == 1 and prev_clk == 0:
            if state:
                state = last_a | last_b
            else:
                state = last_a & last_b

        q = a ^ b ^ state
        result.append({'q': q, 'state': state})
        last_a = a
        last_b = b
        prev_clk = clk

    return result
