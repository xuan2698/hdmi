def reference(vectors):
    out = []
    for row in vectors:
        if isinstance(row, dict):
            L = row.get('L', 0)
            q_in = row.get('q_in', 0)
            r_in = row.get('r_in', 0)
        else:
            try:
                L = row['L']
                q_in = row['q_in']
                r_in = row['r_in']
            except (TypeError, KeyError):
                vals = list(row)
                L = vals[0] if len(vals) > 0 else 0
                q_in = vals[1] if len(vals) > 1 else 0
                r_in = vals[2] if len(vals) > 2 else 0
        L = int(L) & 1
        q_in = int(q_in) & 1
        r_in = int(r_in) & 1
        Q = r_in if L else q_in
        out.append({'Q': Q})
    return out
