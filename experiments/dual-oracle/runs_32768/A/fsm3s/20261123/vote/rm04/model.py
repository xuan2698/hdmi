def reference(vectors):
    state = 0
    nxt = ((0, 1), (2, 1), (0, 3), (2, 1))
    outv = (0, 0, 0, 1)
    result = []
    for row in vectors:
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            inp = row.get('in', 0)
        else:
            inp = row[0] if len(row) > 0 else 0
            reset = row[1] if len(row) > 1 else 0
        if reset:
            state = 0
        else:
            state = nxt[state][1 if inp else 0]
        result.append({'out': outv[state]})
    return result
