def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        reset = row['reset'] if isinstance(row, dict) else row[0]
        if reset:
            q = 0
        else:
            q = (q + 1) % 10
        out.append({'q': q})
    return out
