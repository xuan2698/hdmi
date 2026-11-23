def reference(vectors):
    state = 0
    result = []
    for row in vectors:
        if isinstance(row, dict):
            inp = row.get('in', 0)
            rst = row.get('reset', 0)
        else:
            inp = row[0]
            rst = row[1]

        if rst:
            state = 0
        else:
            if state == 0:
                state = 1 if inp else 0
            elif state == 1:
                state = 2 if inp == 0 else 1
            elif state == 2:
                state = 0 if inp == 0 else 3
            else:
                state = 2 if inp == 0 else 1

        result.append({'out': 1 if state == 3 else 0})
    return result
