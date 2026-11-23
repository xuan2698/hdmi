def reference(vectors):
    state = 0  # A
    results = []
    for row in vectors:
        if isinstance(row, dict):
            rst = int(row.get('reset', 0))
            inp = int(row.get('in', 0))
        else:
            rst = int(row[0])
            inp = int(row[1])
        if rst:
            state = 0
        else:
            if state == 0:
                state = 1 if inp else 0
            elif state == 1:
                state = 1 if inp else 2
            elif state == 2:
                state = 3 if inp else 0
            else:
                state = 1 if inp else 2
        results.append({'out': 1 if state == 3 else 0})
    return results
