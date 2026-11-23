def reference(vectors):
    Q = 0
    result = []
    for row in vectors:
        if isinstance(row, dict):
            L = row.get('L', 0)
            q_in = row.get('q_in', 0)
            r_in = row.get('r_in', 0)
        else:
            L = row[0]
            q_in = row[1]
            r_in = row[2]
        Q = (r_in if L else q_in) & 1
        result.append({'Q': Q})
    return result
