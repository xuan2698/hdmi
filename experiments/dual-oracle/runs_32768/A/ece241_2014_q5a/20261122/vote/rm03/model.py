def reference(vectors):
    state = 0  # 0: no 1 yet, z=0; 1: seen, z=1; 2: seen, z=0
    out = []
    if isinstance(vectors, dict):
        a = vectors.get('areset', 0)
        if isinstance(a, (list, tuple)):
            n = len(a)
            rows = ({'areset': vectors['areset'][i], 'x': vectors['x'][i]} for i in range(n))
        else:
            rows = [vectors]
    else:
        rows = vectors
    for row in rows:
        if isinstance(row, dict):
            areset = int(row.get('areset', 0))
            x = int(row.get('x', 0))
        else:
            areset = int(row[0])
            x = int(row[1])
        if areset:
            state = 0
        else:
            if state == 0:
                state = 1 if x else 0
            elif state == 1:
                state = 2 if x else 1
            else:
                state = 2 if x else 1
        z = 1 if state == 1 else 0
        out.append({'z': z})
    return out
