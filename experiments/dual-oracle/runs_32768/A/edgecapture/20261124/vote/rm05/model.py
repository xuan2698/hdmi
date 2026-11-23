def reference(vectors):
    if isinstance(vectors, dict):
        keys = list(vectors.keys())
        n = len(vectors[keys[0]]) if keys else 0
        rows = [{k: vectors[k][i] for k in keys} for i in range(n)]
    else:
        rows = vectors

    out = 0
    prev = 0
    result = []

    for row in rows:
        if isinstance(row, dict):
            rst = row.get('reset', 0)
            inv = row.get('in', 0)
        else:
            rst = row[0]
            inv = row[1]

        rst = int(rst) & 1
        inv = int(inv) & 0xffffffff

        if rst:
            out = 0
        else:
            out = (out | (prev & (~inv))) & 0xffffffff

        prev = inv
        result.append({'out': out})

    return result
